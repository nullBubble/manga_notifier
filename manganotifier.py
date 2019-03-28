import time
from prettytable import PrettyTable as pt
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

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
fp = webdriver.FirefoxProfile('/home/minh/.mozilla/firefox/xfica4w6.default')

# use profile so we dont have to log in everytime. trying to avoid bot detection on the website. 
driver = webdriver.Firefox(firefox_profile=fp)
driver.implicitly_wait(10)
driver.get("https://mangadex.org")
time.sleep(1.5)

with open("log","w") as f:
    for manga in mangalist:
        driver.find_element_by_id('quick_search_input').send_keys(manga['name'], Keys.RETURN)
        #clicks on the correct search result
        element = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.LINK_TEXT, manga['name'])))
        driver.find_element_by_link_text(manga['name']).click()
        #gets text of the latest chapter. account settings in mangadex must only filter by english
        element = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.chapter-container > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > a:nth-child(1)')))
        cur_chapter = driver.find_element_by_css_selector('.chapter-container > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > a:nth-child(1)').text
        #split chapter name. search for index of the keyword "Ch.", the actual chapter follows that therefore the increment. format example "Vol. 10.5 Ch. 46.5 - Extra pages"
        cur_chapter = cur_chapter.split()
        cur_chapter_number = cur_chapter[cur_chapter.index("Ch.") + 1]
        table.add_row([manga['name'],cur_chapter_number,manga['chapter']])
        time.sleep(3.5)
    f.write(table.get_string())
#f.write("\nNeed to check Grand Blue and Kekkon Yubiwa on Mangahere.\n")

driver.close()
driver.quit()