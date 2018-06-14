# -*- coding: utf-8 -*-

import os, sys, json

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests


def qprint(msg):
    print(':: ' + msg, file=sys.stderr, flush=True)


def qopen(fname, mode='r', verbose=True):
    if verbose:
        if mode == 'w':
            qprint('writing {}'.format(fname))
        else:
            qprint('reading {}'.format(fname))

    return open(fname, mode)


def write_json(in_dict, out_json):

    fout = qopen(out_json, 'w')
    print(json.dumps(in_dict, sort_keys=True, indent=2), file=fout)
    fout.close()


def read_json(in_json):

    return json.loads(qopen(in_json).read())


def write_text(in_str, out_name):

    fout = qopen(out_name, 'w')
    print(in_str, file=fout)
    fout.close()


def read_text(in_name):

    return qopen(in_name).read()


# -------------------------------------------------------------------------

def login_genomeweb(driver, config):

    elem = driver.find_element_by_xpath('//input[@id="edit-name"]')
    elem.send_keys(config['login_username'])
    elem = driver.find_element_by_xpath('//input[@id="ignore"]')
    elem.click()
    elem = driver.find_element_by_xpath('//input[@id="edit-pass"]')
    elem.send_keys(config['login_password'])
    elem = driver.find_element_by_xpath('//input[@id="edit-submit"]')
    elem.click()

# -------------------------------------------------------------------------

def login_tmclibrary(driver, config):

    elem = driver.find_element_by_xpath('//input[@name="user"]')
    elem.send_keys(config['login_username'])
    elem = driver.find_element_by_xpath('//input[@name="pass"]')
    elem.send_keys(config['login_password'])
    elem = driver.find_element_by_xpath('//input[@value="Submit"]')
    elem.click()

# -------------------------------------------------------------------------

def login_6park(driver, config):

    elem = driver.find_element_by_xpath('//input[@name="username"]')
    elem.send_keys(config['login_username'])
    elem = driver.find_element_by_xpath('//input[@name="password"]')
    elem.send_keys(config['login_password'])
    elem = driver.find_element_by_xpath('//input[@name="dologin"]')
    elem.click()


# -------------------------------------------------------------------------

def get_cookies(in_config_json, out_cookie_json, headless=True):

    config = read_json(in_config_json)

    try:

        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")

        qprint('open webdriver')
        driver = webdriver.Chrome(chrome_options=chrome_options)

        qprint('get {}'.format(config['url_login']))
        driver.get(config['url_login'])

        qprint('perform login')
        if config['host'] == 'genomeweb':
            login_genomeweb(driver, config)
        elif config['host'] == 'tmclibrary':
            login_tmclibrary(driver, config)
        elif config['host'] == '6park':
            login_6park(driver, config)
        time.sleep(10)

        qprint('get cookies')
        cookies = driver.get_cookies()
        write_json(cookies, out_cookie_json)

        qprint('close webdriver')
        driver.close()

    except Exception as e:

        qprint('*ERROR* ' + str(e))





if __name__ == '__main__':

    in_config_json, out_cookie_json, headless = sys.argv[1:4]
    headless = False if headless == 'False' else True
    get_cookies(in_config_json, out_cookie_json, headless)

    # get_cookies('cred.genomeweb.json', 'cookies.genomeweb.json')
    # get_cookies('cred.tmclibrary.json', 'cookies.tmclibrary.json')
    # get_cookies('cred.6park.json', 'cookies.6park.json', headless=False)



# end
