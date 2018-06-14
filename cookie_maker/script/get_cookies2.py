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

    out_dict = json.loads(qopen(in_json).read())
    return out_dict


def write_text(in_str, out_json):

    fout = qopen(out_json, 'w')
    print(in_str, file=fout)
    fout.close()


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


def test_genomeweb(cookies):

    test_url = 'https://www.genomeweb.com/sequencing/ancient-interbreeding-among-chimpanzees-bonobos-revealed-genome-analysis?utm_medium=TrendMD&utm_campaign=0&utm_source=TrendMD&trendmd-shared=0#.WyGEUXUbNhE'

    s = requests.Session()
    for c in cookies:
        s.cookies.set(c['name'], c['value'])

    r = s.get(test_url)

    for line in r.text.split('\n'):
        if 'schema:articleBody' in line:
            print(line.rstrip())

    if 'paywall-box' not in r.text:
        qprint('Success, cookie is working!')
    else:
        qprint('Failed, cookie is NOT working!')

# -------------------------------------------------------------------------

def login_tmclibrary(driver, config):

    elem = driver.find_element_by_xpath('//input[@name="user"]')
    elem.send_keys(config['login_username'])
    elem = driver.find_element_by_xpath('//input[@name="pass"]')
    elem.send_keys(config['login_password'])
    elem = driver.find_element_by_xpath('//input[@value="Submit"]')
    elem.click()

    time.sleep(10)


def test_tmclibrary(cookies):

    test_url = 'https://www.nature.com.ezproxyhost.library.tmc.edu/articles/s41586-018-0172-5'

    s = requests.Session()
    for c in cookies:
        s.cookies.set(c['name'], c['value'])

    r = s.get(test_url, verify=False)

    # for line in r.text.split('\n'):
    #     if 'schema:articleBody' in line:
    #         print(line.rstrip())

    write_text(r.text, 'foo.html')

    test_text = 'Finally, although there are ice core records throughout Antarctica'
    if test_text in r.text:
        qprint('Success, cookie is working!')
    else:
        qprint('Failed, cookie is NOT working!')


# -------------------------------------------------------------------------


def get_cookies(in_config_json, out_cookie_json, headless=False):

    config = read_json(in_config_json)

    try:

        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")

        qprint('open webdriver')
        driver = webdriver.Chrome(chrome_options=chrome_options)

        qprint('loading {}'.format(config['url_login']))
        driver.get(config['url_login'])

        qprint('perform login')
        # login_genomeweb(driver, config)
        login_tmclibrary(driver, config)

        qprint('get cookies')
        cookies = driver.get_cookies()

        qprint('test cookies')
        # test_genomeweb(cookies)
        test_tmclibrary(cookies)
        write_json(cookies, out_cookie_json)

        qprint('close webdriver')
        driver.close()

    except Exception as e:

        qprint('*ERROR* ' + str(e))





if __name__ == '__main__':




    # get_cookies('cred.genomeweb.json', 'cookies.genomeweb.json')
    get_cookies('cred.tmclibrary2.json', 'cookies.tmclibrary.json')



# end
