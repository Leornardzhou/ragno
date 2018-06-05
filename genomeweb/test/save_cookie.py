from selenium import webdriver
import requests
import time
from selenium.webdriver.common import action_chains, keys
import json



def save_cookie(in_credential_name, out_cookie_name):

    login_url = 'https://www.genomeweb.com/user/login?click_id=UL_Login&type=Login_Block'
    logout_url = 'https://www.genomeweb.com/user/logout'

    print(':: loading {}'.format(in_credential_name))
    cred = json.loads(open(in_credential_name).read())
    print(cred)

    print(':: get url {}'.format(login_url))
    # driver = webdriver.PhantomJS()
    driver = webdriver.Chrome()
    driver.get(login_url)

    elem = driver.find_element_by_xpath('//input[@id="edit-name"]')
    elem.send_keys(cred['username'])
    time.sleep(1)

    elem = driver.find_element_by_xpath('//input[@id="ignore"]')
    elem.click()
    time.sleep(1)

    elem = driver.find_element_by_xpath('//input[@id="edit-pass"]')
    elem.send_keys(cred['password'])
    time.sleep(1)

    elem = driver.find_element_by_xpath('//input[@id="edit-submit"]')
    elem.click()
    time.sleep(1)

    driver.get('https://www.genomeweb.com/regulatory-news/european-data-protection-law-brings-new-responsibilities-possibilities-genomics#.WxRsCFMvzYI')
    time.sleep(3)

    print(':: extract cookies')
    cookie = driver.get_cookies()
    print(cookie)
    print(len(cookie))

    print(':: write cookies to {}'.format(out_cookie_name))
    fout = open(out_cookie_name, 'w')
    print(json.dumps(cookie, sort_keys=True), file=fout)
    fout.close()

    time.sleep(60)

    print(':: logout {}'.format(logout_url))
    driver.get(logout_url)


    driver.close()


if __name__ == '__main__':

    save_cookie('genomeweb.json', 'cookies.json')
