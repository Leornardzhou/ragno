'''Handy tools commonly used by other modules (independent of website). '''

from selenium import webdriver
import sys
import json
import time
import random
import requests
import os
import shutil


def clean_dir(target_dir, verbose=True):
    # keep the target_dir and clean everything inside

    if verbose:
        print_message('clean up "{}"'.format(target_dir))
    for item in os.listdir(target_dir):
        item = target_dir + '/' + item
        if os.path.isdir(item):
            shutil.rmtree(item)
        else:
            os.remove(item)


def start_driver(driver_name, wait_time=5, verbose=False, download_dir=None):

    # clean up download_dir
    clean_dir(download_dir, verbose=verbose)

    if verbose:
        print_message('open {} browser'.format(driver_name))

    if driver_name == 'chrome':
        if download_dir:
            opts = webdriver.ChromeOptions()
            prefs = {
                "download.default_directory": download_dir,
                'safebrowsing.enabled': True,
            }
            opts.add_experimental_option('prefs', prefs)
            opts.add_argument(
                '--safebrowsing-disable-download-protection'
            )
            driver = webdriver.Chrome(chrome_options=opts)
        else:
            driver = webdriver.Chrome()

    elif driver_name == 'phantomjs':
        # does not support download dir sepcification
        driver = webdriver.PhantomJS()

    elif driver_name == 'firefox':
        if download_dir:
            profile = webdriver.FirefoxProfile()
            profile.set_preference("browser.download.folderList", 2)
            profile.set_preference("browser.download.manager.showWhenStarting",
                                   False)
            profile.set_preference("browser.download.dir", download_dir)
            profile.set_preference("browser.helperApps.neverAsk.saveToDisk",
                                   "application/octet-stream")
            profile.set_preference("browser.helperApps.neverAsk.openFile",
                                   "application/octet-stream")
            driver = webdriver.Firefox(firefox_profile=profile)
        else:
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


def save_html(driver, fname, verbose=True):
    if verbose:
        print_message('writing html {}'.format(fname))
    elem = driver.find_element_by_xpath("//*")
    source_code = elem.get_attribute("outerHTML")
    with open(fname, 'w') as f:
        print(source_code, file=f)


def download_file(url, fname, verbose=True, chunk_size=1024):
    if verbose:
        print_message('saving {} to {}'.format(url, fname))
    r = requests.get(url, stream=True)
    with open(fname, 'wb') as f:
        for chunk in r.iter_content(chunk_size=chunk_size):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
    r.close()


def print_message(msg):
    print('> ' + msg, file=sys.stderr, flush=True)


def save_json(data, fname, verbose=True):
    dirname = fname.rsplit('/',1)[0]
    os.makedirs(dirname, exist_ok=True)
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
