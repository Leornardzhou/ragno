'''Handy tools commonly used by other modules (independent of website). '''

from selenium import webdriver
import sys
import json
import time
import random


def start_driver(driver_name, wait_time=5, verbose=False):
    if verbose:
        print_message('open {} browser'.format(driver_name))
    if driver_name == 'chrome':
        driver = webdriver.Chrome()
    elif driver_name == 'phantomjs':
        driver = webdriver.PhantomJS()
    elif driver_name == 'firefox':
        driver = webdriver.Firefox()
    driver.implicitly_wait(wait_time)
    return driver


def close_driver(driver, verbose=False):
    if verbose:
        print_message('close browser')
    driver.quit()


def open_url(driver, url, verbose=False, wait_time=0, reopen=False):
    if driver.current_url == url and reopen == False:
        return
    if verbose:
        print_message('openning URL: ' + url)
    driver.get(url)


def print_message(msg):
    print('> ' + msg, file=sys.stderr, flush=True)


def save_json(data, fname, verbose=True):
    if verbose:
        print_message('writing json {}'.format(fname))
    with open(fname, 'w') as f:
        print(json.dumps(data, sort_keys=True), file=f)


def load_json(fname, verbose=True):
    if verbose:
        print_message('loading json {}'.format(fname))
    return json.loads(open(fname).read())


def wait(time1, time2=None, verbose=False):
    if not time2:
        wait_time = time1
    else:
        wait_time = time1 + random.random() * abs(time2 - time1)
    if verbose:
        print_message('wait for {0:.2f} seconds ...'.format(wait_time))
    time.sleep(wait_time)


def save_screenshot(driver, fname):
    print_message('screenshot saved to ' + fname)
    driver.save_screenshot(fname)
