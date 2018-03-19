'''Crawl a number of pages of proxies from https://www.proxydocker.com/en/

The output is saved to ../data directory (proxydocker.yyyymmddHHMM.proxies.json)
'''

import os
from os.path import dirname, abspath
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import date
from pyvirtualdisplay import Display   # linux only
import json
import time
import requests
import datetime
import test_proxy
import gzip


lang = 'en'
main_url = 'https://www.proxydocker.com/{}/proxylist/type/HTTP'.format(lang)
root_dir = dirname(dirname(abspath(__file__)))
data_dir = '{}/data'.format(root_dir)


def save_json(proxy_dict, fname):
    '''Save a proxy dictionary as JSON file.'''

    print('writing output json ' + fname)
    if fname.endswith('.gz'):
        fout = gzip.open(fname, 'wb')
        fout.write(json.dumps(proxy_dict, sort_keys=True).encode('utf-8'))
    else:
        fout = open(fname, 'w')
        print(json.dumps(proxy_dict, sort_keys=True), file=fout)
    fout.close()


def goto_page(driver, page_id, html_out, nretry_max=10, sleep_time=3):
    '''Download a page with given page ID (retry at maximum nretry_max times).'''

    nretry = 0
    nproxy = 0
    while nretry < nretry_max and nproxy == 0:
        print('get {} page {} (retry={})'.format(main_url, page_id, nretry))
        try:
            driver.get(main_url)
            driver.execute_script(
                'document.getElementById(\'page_input\').value = {}'
                .format(page_id))
            driver.execute_script(
                'document.getElementById(\'pagination\').submit()')
            time.sleep(sleep_time)
            nproxy = len(driver.find_elements_by_xpath(
                '//tbody/tr/td/a[starts-with(@href, "/{}/proxy/")]'.format(lang)))
        except:
            pass
        nretry += 1

    if nproxy:
        data = driver.find_element_by_xpath('/*').get_attribute('outerHTML')
        fout = open(html_out, 'w')
        print(data, file=fout)
        fout.close()

    return nproxy


def serial_test_proxy(proxy_url, test_url='http://icanhazip.com',
               timeout=15, nretry_max=3):
    '''Test if proxy is effective and return elapse of test time.'''

    print(':: testing {} ... '.format(proxy_url), end='', file=sys.stderr)
    elapsed = -1

    nretry = 0
    while nretry < nretry_max:
        try:
            r = requests.get(test_url, proxies={'http': proxy_url},
                             timeout=timeout)
            if r.ok and r.text.rstrip() == proxy_url.split(':')[0]:
                elapsed = r.elapsed.total_seconds()
        except:
            # no subdivision of error here
            pass
        nretry += 1

    if elapsed > 0:
        print('success in {} seconds'.format(elapsed), file=sys.stderr)
    else:
        print('failed', file=sys.stderr)

    return elapsed


def get_proxy_list(driver, html_in, with_test=True):
    '''Extract proxies and attributes from a local html file.'''

    # use local file to avoid staled element in cache
    driver.get('file://' + html_in)

    print('processing ' + html_in)

    proxy_dict = dict()
    elem_list = driver.find_elements_by_xpath(
        '//tbody/tr/td/a[starts-with(@href, "/{}/proxy/")]'.format(lang))
    for elem in elem_list:
        proxy_url = elem.get_attribute("href").split('/')[-1]
        ptype = (elem.find_element_by_xpath('../../td[2]').
                 get_attribute('innerHTML').replace(' ','').replace('\n',''))
        panonymity = (elem.find_element_by_xpath('../../td[3]').
                      get_attribute('innerHTML').replace(' ','').replace('\n',''))
        ptimeout = int(elem.find_element_by_xpath('../../td[4]/span/span')
                    .get_attribute('style').split(': ')[-1].replace('%;',''))
        pcountry = (elem.find_element_by_xpath('../../td[5]')
                    .text.replace('\n','').strip())
        pcity = (elem.find_element_by_xpath('../../td[6]')
                 .text.replace('\n','').strip())
        if pcountry == '':
            pcountry = 'Unknown'
        proxy_dict[proxy_url] = {
            'type': ptype, 'anonymity': panonymity,
            'country': pcountry, 'city': pcity, 'timeout': ptimeout,
        }

    return proxy_dict


def merge_json(timestamp, with_test=False):
    '''Merge all jsons with the same timestamp (optionally vaildate and filter
    proxies).
    '''

    json_out = '{}/proxydocker.{}.proxies.json.gz'.format(data_dir, timestamp)
    proxy_dict = {}
    for fname in os.listdir(data_dir):
        if not fname.startswith('proxydocker.{}.proxies.page'
                                .format(timestamp)):
            continue
        fname = '{}/{}'.format(data_dir, fname)
        # print('merging ' + fname, file=sys.stderr)
        tmp_dict = json.loads(open(fname).read())
        proxy_dict.update(tmp_dict)

    for fname in os.listdir(data_dir):
        if not fname.startswith('proxydocker.{}.proxies.page'
                                .format(timestamp)):
            continue
        os.remove('{}/{}'.format(data_dir,fname))

    print('collected {} proxies'.format(len(proxy_dict)), file=sys.stderr)

    if with_test:
        exclude_proxies = set()
        for proxy in proxy_dict:
            elapse = serial_test_proxy(proxy)
            if elapse < 0:
                exclude_proxies.add(proxy)
            else:
                proxy_dict[proxy]['elapse'] = elapse
        for proxy in exclude_proxies:
            proxy_dict.pop(proxy)
        print('validated {} proxies successful'
              .format(len(proxy_dict)), file=sys.stderr)

    save_json(proxy_dict, json_out)


def proxydocker(npage):
    '''Extract proxies in a number of pages from proxydocker.com'''

    # display = Display(visible=0, size=(1024,768))
    # display.start()

    driver = webdriver.PhantomJS()
    # driver = webdriver.Chrome()
    proxy_dict = {}
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M")
    os.makedirs(data_dir, exist_ok=True)
    fname_prefix = '{}/proxydocker.{}.proxies'.format(data_dir, timestamp)
    html_tmp = 'Null'

    try:
        for i in range(1, npage+1):
            html_tmp = '{}.page{}.tmp'.format(fname_prefix, i)
            json_out = '{}.page{}.json'.format(fname_prefix, i)
            nproxy = goto_page(driver, i, html_tmp)
            if nproxy:
                proxy_dict = get_proxy_list(driver, html_tmp)
                if len(proxy_dict):
                    save_json(proxy_dict, json_out)
                os.remove(html_tmp)

    except:
        print('*ERROR*', file=sys.stderr)
        raise

    finally:
        driver.close()
        if os.path.isfile(html_tmp):
            os.remove(html_tmp)
        # display.stop()

    # merge jsons (better validation with multiprocessing)
    merge_json(timestamp)
    return timestamp


if __name__ == '__main__':

    npage = int(sys.argv[1])
    timestamp = proxydocker(npage)
    # test_proxy.test_all_proxy(timestamp)
