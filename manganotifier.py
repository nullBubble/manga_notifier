import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
    
#from the manga list create separated manga list and chapter list with the same indices
mlist, clist = [], []
f = open("Mangalist","r")
output = f.readlines()
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


driver = webdriver.Firefox()
driver.implicitly_wait(10)
driver.get("https://mangadex.org/login")
#log in because search does not work as a gues
driver.find_element_by_id('login_username').send_keys(usr)
driver.find_element_by_id('login_password').send_keys(pw)
driver.find_element_by_id('login_button').click()

driver.find_element_by_id('quick_search_input').send_keys(mlist[0], Keys.RETURN)
#clicks on the first search result which should be the correct manga if full name is given in mangalist
time.sleep(2)
driver.find_element_by_css_selector('a.ml-1').click()
#gets text of the latest chapter
time.sleep(2)
cur_chapter = driver.find_element_by_css_selector('.chapter-container > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > a:nth-child(1)').text

#split chapter name. search for index of the keyword "Ch.", the actual chapter follows that therefore the increment. format example "Vol. 10.5 Ch. 46.5 - Extra pages"
cur_chapter = cur_chapter.split()
cur_chapter_number = cur_chapter[cur_chapter.index("Ch.") + 1]
print(cur_chapter)
print(cur_chapter_number)