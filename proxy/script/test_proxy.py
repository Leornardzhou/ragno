import os
import requests
import sys
import multiprocessing
from multiprocessing import Pool
import json
import time
import random

def test_all_proxy(timestamp, domain='proxydocker'):

    json_in = '../data/{}.{}.proxies.json'.format(domain, timestamp)
    list_out = '../data/{}.{}.proxies.valid.list'.format(domain, timestamp)
    data = json.loads(open(json_in).read())

    proxy_list = sorted(list(data.keys()))
    print(len(proxy_list))
    # proxy_list = [x for x in range(100)]
    p = Pool(processes=8)
    r = [p.apply_async(test_proxy, args=(x,)) for x in proxy_list]
    output = [x.get() for x in r]
    output = [x for x in output if x != 'Null']

    print('writing ' + list_out, file=sys.stderr)
    fout = open(list_out, 'w')
    for proxy in output:
        print(proxy, file=fout)
    fout.close()


def foo(proxy_url):
    time.sleep(1 + random.uniform(0,3))
    print(proxy_url, flush=True)
    return proxy_url


def test_proxy(proxy_url, test_url='http://icanhazip.com',
               timeout=15, nretry_max=3):
    '''Test if proxy is effective and return elapse of test time.'''

    nretry = 0
    while nretry < nretry_max:
        print(':: testing {} ... (retry={}) [{}]'
              .format(proxy_url, nretry, multiprocessing.current_process()),
              file=sys.stderr, flush=True)
        try:
            r = requests.get(test_url, proxies={'http': proxy_url},
                             timeout=timeout)
            if r.ok and r.text.rstrip() == proxy_url.split(':')[0]:
                return proxy_url
        except:
            pass

        nretry += 1
        time.sleep(1)

    return 'Null'


if __name__ == '__main__':

    timestamp = sys.argv[1]
    test_all_proxy(timestamp)
