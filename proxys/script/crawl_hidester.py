# -*- coding: utf-8 -*-

import os, sys, json, gzip, time
from selenium import webdriver

# -------------------------------------------------------------------------

def write_text(text, text_name, verbose=True):

    if verbose:
        qprint('write ' + text_name)
    if text_name.endswith('.gz'):
        fout = gzip.open(text_name, 'wb')
        fout.write((text+'\n').encode('utf-8'))
    else:
        fout = open(text_name, 'w')
        fout.write(text+'\n')
    fout.close()

# -------------------------------------------------------------------------

def read_text(text_name, verbose=True):

    if verbose:
        qprint('read ' + text_name)
    if text_name.endswith('.gz'):
        text = gzip.open(text_name).read().decode('utf-8')
    else:
        text = open(text_name).read()
    return text

# -------------------------------------------------------------------------

def get_timestamp(fmt_str="%Y%m%d%H%M"):

    timestamp = datetime.datetime.now().strftime(fmt_str)
    return timestamp

# -------------------------------------------------------------------------

def qprint(msg, verbose=True):
    print(':: ' + msg, file=sys.stderr, flush=True)

# -------------------------------------------------------------------------

def qopen(fname, mode='r', verbose=True):

    if verbose:
        if 'w' in mode:
            qprint('writing {}'.format(fname))
        else:
            qprint('reading {}'.format(fname))

    if fname.endswith('.gz'):
        return gzip.open(fname, mode)
    else:
        return open(fname, mode)


# -------------------------------------------------------------------------

def write_json(data, json_name, verbose=True):
    if verbose:
        qprint('write ' + json_name)
    if json_name.endswith('.gz'):
        fout = gzip.open(json_name, 'wb')
        fout.write((json.dumps(data, sort_keys=True) + '\n').encode('utf-8'))
    else:
        fout = open(json_name, 'w')
        fout.write(json.dumps(data, sort_keys=True) + '\n')
    fout.close()

# -------------------------------------------------------------------------

def read_json(json_name, verbose=True):
    if verbose:
        qprint('read ' + json_name)
    if json_name.endswith('.gz'):
        data = json.loads(gzip.open(json_name).read().decode('utf-8'))
    else:
        data = json.loads(open(json_name).read())
    return data


# -------------------------------------------------------------------------

def get_proxy_all_pages(driver):

    out = dict()

    url = 'https://hidester.com/proxylist'

    qprint('get url {}'.format(url))
    driver.get(url)
    time.sleep(3)

    for i in range(1,6):
        qprint('open page {}'.format(i))
        driver.execute_script("window.scrollTo(0, 1400)")
        for a in driver.find_elements_by_xpath('//a[@ng-click="selectPage(page.number, $event)"]'):
            if a.text == str(i):
                a.click()
                break
        time.sleep(2)

        for tr in driver.find_elements_by_xpath('//tbody/tr'):
            tmp = []
            for td in tr.find_elements_by_xpath('./td'):
                tmp.append(td.text)
            if len(tmp) == 0:
                continue
            key = '{}:{}'.format(tmp[1], tmp[2])
            value = {
                'last_check': tmp[0], 'country': tmp[3], 'type': tmp[4],
                'ping': tmp[6], 'anonymity': tmp[7], 'google': tmp[8],
            }
            out[key] = value

        qprint('found {} proxies'.format(len(out)))

    return out

# -------------------------------------------------------------------------

def write_output(data, out_json):

    out = []
    for key, value in sorted(data.items()):
        out.append('{}\t{}'.format(
            key, json.dumps(value, sort_keys=True)))

    if not out_json.endswith('.gz'):
        out_json = out_json + '.gz'
    fout = qopen(out_json, 'wb')
    fout.write(('\n'.join(out)+'\n').encode('utf-8'))
    fout.close()


# -------------------------------------------------------------------------

def crawl_hidester(out_json):

    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    options.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=options)

    data = get_proxy_all_pages(driver)
    qprint('total number of proxies = {}'.format(len(data)))

    write_output(data, out_json)

    driver.close()

# -------------------------------------------------------------------------

if __name__ == '__main__':

    out_json = sys.argv[1]
    crawl_hidester(out_json)


# end
