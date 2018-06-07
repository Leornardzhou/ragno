from selenium import webdriver
import requests
import time
from selenium.webdriver.common import action_chains, keys
import json

in_credential_name = 'genomeweb.json'
out_cookie_name = 'foo.json'

login_url = 'https://www.genomeweb.com/user/login?click_id=UL_Login&type=Login_Block'
logout_url = 'https://www.genomeweb.com/user/logout'

print(':: loading {}'.format(in_credential_name))
cred = json.loads(open(in_credential_name).read())
print(cred)

print(':: get url {}'.format(login_url))
# driver = webdriver.Chrome()
driver = webdriver.PhantomJS()
driver.get(login_url)

elem = driver.find_element_by_xpath('//input[@id="edit-name"]')
elem.send_keys(cred['username'])
elem = driver.find_element_by_xpath('//input[@id="ignore"]')
elem.click()
elem = driver.find_element_by_xpath('//input[@id="edit-pass"]')
elem.send_keys(cred['password'])
elem = driver.find_element_by_xpath('//input[@id="edit-submit"]')
elem.click()
cookie = driver.get_cookies()

fout = open('cookies2.json', 'w')
print(json.dumps(cookie, sort_keys=True, indent=2), file=fout)
fout.close()

driver.close()
