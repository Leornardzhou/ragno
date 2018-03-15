'''Crawl list of proxies from https://www.proxydocker.com/en/
'''

import os
import sys
from selenium import webdriver
from datetime import date
from pyvirtualdisplay import Display   # linux only
import json
import time
import requests
import datetime

main_url = 'https://www.proxydocker.com/en/proxylist/type/HTTP'
data_dir = '../data'


def save_json(proxy_dict, fname):
    '''Save a proxy dictionary as JSON file.'''

    print('writing output json ' + fname)
    fout = open(fname, 'w')
    print(json.dumps(proxy_dict, sort_keys=True), file=fout)
    fout.close()


def goto_page(driver, page_id, html_out, nretry_max=10):
    '''Try save a page with page ID (retry at maximum nretry_max times).'''

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
            nproxy = len(driver.find_elements_by_xpath(
                '//tbody/tr/td/a[starts-with(@href, "/en/proxy/")]'))
        except:
            nretry += 1

    if nproxy:
        data = driver.find_element_by_xpath('/*').get_attribute('outerHTML')
        fout = open(html_out, 'w')
        print(data, file=fout)
        fout.close()

    return nproxy


def test_proxy(proxy_url, test_url='http://icanhazip.com', timeout=15):
    '''Test if proxy is effective and return elapse of test time.'''

    print(':: testing {} ... '.format(proxy_url), end='', file=sys.stderr)
    elapsed = -1
    try:
        r = requests.get(test_url, proxies={'http': proxy_url}, timeout=timeout)
        if r.ok and r.text.rstrip() == proxy_url.split(':')[0]:
            elapsed = r.elapsed.total_seconds()
    except:
        # no subdivision of error here
        pass

    if elapsed > 0:
        print('success in {} seconds'.format(elapsed), file=sys.stderr)
    else:
        print('failed', file=sys.stderr)

    return elapsed


def get_proxy_list(driver, html_in, with_test=True):

    # use local file to avoid staled element in cache
    driver.get(html_in)

    print('processing ' + html_in)

    proxy_dict = dict()
    elem_list = driver.find_elements_by_xpath(
        '//tbody/tr/td/a[starts-with(@href, "/en/proxy/")]')
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


def merge_json(timestamp, with_test=True):

    json_out = '{}/proxydocker.{}.proxies.json'.format(data_dir, timestamp)
    proxy_dict = {}
    for fname in os.listdir(data_dir):
        if not fname.startswith('proxydocker.{}.proxies.page'
                                .format(timestamp)):
            continue
        fname = '{}/{}'.format(data_dir, fname)
        print('merging ' + fname, file=sys.stderr)
        tmp_dict = json.loads(open(fname).read())
        proxy_dict.update(tmp_dict)
        # os.remove(fname)

    print('collected {} proxies'.format(len(proxy_dict)), file=sys.stderr)

    if with_test:
        exclude_proxies = set()
        for proxy in proxy_dict:
            elapse = test_proxy(proxy)
            if elapse < 0:
                exclude_proxies.add(proxy)
            else:
                proxy_dict[proxy]['elapse'] = elapse
        for proxy in exclude_proxies:
            proxy_dict.pop(proxy)
        print('tested {} proxies successful'
              .format(len(proxy_dict)), file=sys.stderr)

    save_json(proxy_dict, json_out)


def proxydocker(npage):

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

    # merge jsons (better with multiprocessing)
    # merge_json(timestamp)

if __name__ == '__main__':

    npage = int(sys.argv[1])
    proxydocker(npage)
