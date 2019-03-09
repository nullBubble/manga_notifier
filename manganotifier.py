from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def list_to_array(list):
    f = open(list,"r")
    output = f.read()
    arr = [x.strip() for x in output.split(',')]
    f.close()
    return arr
    
#create array from the manga list and corresponding chapter list in the same order in .csv format
mlist, clist = [], []
mlist = list_to_array("Mangalist")
clist = list_to_array("Chapterlist")

#get log in credentials from cred file in same directory
f = open("cred", "r")
res = f.readlines()
usr = res[0].strip()
pw = res[1].strip()


driver = webdriver.Firefox()
driver.get("https://mangadex.org/login")

#log in because search does not work as a gues
driver.find_element_by_id('login_username').send_keys(usr)
driver.find_element_by_id('login_password').send_keys(pw)
driver.find_element_by_id('login_button').click()

driver.find_element_by_id('quick_search_input').send_keys(mlist[0], Keys.RETURN)