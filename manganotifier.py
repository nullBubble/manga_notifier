import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

#from the manga list create separated manga list and chapter list with the same indices
mlist, clist = [], []
f = open("Mangalist","r")
output = f.readlines()
f.close()
#this removes the trailing \n character and the rsplit creates for every entry a list with name in the first and ch. number in the 2nd place
output = [line.rstrip('\n').rsplit(' ',1) for line in output]

#separate tuples into the separate lists
for x in range(len(output)):
    mlist.append(output[x][0])
    clist.append(output[x][1])

#get log in credentials from cred file in same directory
f = open("cred", "r")
res = f.readlines()
usr = res[0].strip()
pw = res[1].strip()
f.close()

options = Options()
options.headless = True

driver = webdriver.Firefox(options=options)
driver.implicitly_wait(10)
driver.get("https://mangadex.org/login")
#log in because search does not work as a guest
element = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, 'login_username')))
driver.find_element_by_id('login_username').send_keys(usr)
driver.find_element_by_id('login_password').send_keys(pw)
driver.find_element_by_id('login_button').click()

time.sleep(1)
f = open("log","w")

for x in range(len(mlist)):
    driver.find_element_by_id('quick_search_input').send_keys(mlist[x], Keys.RETURN)
    #clicks on the first search result which should be the correct manga if full name is given in mangalist
    element = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.ml-1')))
    driver.find_element_by_css_selector('a.ml-1').click()
    #gets text of the latest chapter. account settings in mangadex must only filter by english
    element = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.chapter-container > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > a:nth-child(1)')))
    cur_chapter = driver.find_element_by_css_selector('.chapter-container > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > a:nth-child(1)').text
    #split chapter name. search for index of the keyword "Ch.", the actual chapter follows that therefore the increment. format example "Vol. 10.5 Ch. 46.5 - Extra pages"
    cur_chapter = cur_chapter.split()
    cur_chapter_number = cur_chapter[cur_chapter.index("Ch.") + 1]
    if float(cur_chapter_number) > float(clist[x]):
        f.write(mlist[x]+" latest Chapter is "+cur_chapter_number +". Your current chapter is "+clist[x]+".\n")
    else:
        f.write("No new chapters for "+mlist[x]+".\n")
    time.sleep(2.5)

f.write("Need to check Grand Blue and Kekkon Yubiwa on Mangahere.\n")
f.close()

driver.close()
driver.quit()