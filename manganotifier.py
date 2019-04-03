import time
import smtplib
import config
import datetime
from selenium import webdriver
from prettytable import PrettyTable as pt
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


def send_mail(sub,filename):
    try:
        message = MIMEMultipart()
        message['From'] = config.SENDER
        message['To'] = config.RECEIVER
        message['Subject'] = sub

        with open(filename, "rb") as f:
            part = MIMEApplication(f.read(),Name=filename)
        part['Content-Disposition'] = 'attachment; filename="%s"' % filename
        message.attach(part)

        svr = smtplib.SMTP('smtp.gmail.com:587')
        svr.ehlo()
        svr.starttls()
        svr.login(config.SENDER, config.PASSWORD)
        svr.sendmail(config.SENDER, config.RECEIVER, message.as_string())
        svr.quit()
        print("Success")
    except:
        print("Fail")

with open("Mangalist","r") as f:
    output = f.readlines()

# this removes the trailing \n character and the rsplit creates for every entry a list with name in the first and ch. number in the 2nd place
# from this ["name chapter\n", ...]  to this [ ["name","chapter"], ... ]
output = [line.rstrip('\n').rsplit(' ',1) for line in output]

# create key value list from output
mangalist = []
for i in range(len(output)):
    manga = {"name": output[i][0],"chapter":output[i][1]}
    mangalist.append(manga)

# creating table for log file
table = pt()
table.field_names = ["Name", "Current", "Latest"]

options = Options()
options.headless = True
fp = webdriver.FirefoxProfile('/path/to/profile')

# use profile so we dont have to log in everytime. trying to avoid bot detection on the website. 
driver = webdriver.Firefox(firefox_profile=fp,options=options)
driver.implicitly_wait(10)
driver.get("https://mangadex.org")
time.sleep(1.5)

with open("log.txt","w") as f:
        i = 0
    for manga in mangalist:
        driver.find_element_by_id('quick_search_input').send_keys(manga['name'], Keys.RETURN)
        #clicks on the correct search result
        element = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.LINK_TEXT, manga['name'])))
        driver.find_element_by_link_text(manga['name']).click()
        #gets text of the latest chapter. account settings in mangadex must only filter by english
        element = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.chapter-container > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > a:nth-child(1)')))
        latest_chapter = driver.find_element_by_css_selector('.chapter-container > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > a:nth-child(1)').text
        #split chapter name. search for index of the keyword "Ch.", the actual chapter follows that therefore the increment. format example "Vol. 10.5 Ch. 46.5 - Extra pages"
        latest_chapter = latest_chapter.split()
        latest_chapter_number = latest_chapter[latest_chapter.index("Ch.") + 1]
        table.add_row([manga['name'][:23],manga['chapter'],latest_chapter_number])
        # sleep timer so that we dont send too many requests in a short amount of time and getting blocked by the website
        print("Processing %i" % i)
        time.sleep(3.5)
        i = i+1
    f.write(table.get_string())

with open("log.txt","r") as f:
    msg = f.read()
    
current_time = datetime.datetime.now()
month = current_time.strftime("%B")
day = current_time.strftime("%d")
sub = "%s. %s Manga Recap" % (day,month)

send_mail(sub, "log.txt")
driver.close()
driver.quit()
