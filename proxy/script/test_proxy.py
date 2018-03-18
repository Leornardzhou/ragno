'''Validate all proxies in a json with gievn timestamp.
'''

import os
from os.path import dirname, abspath
import requests
import sys
import multiprocessing
from multiprocessing import Pool
import json
import time
import random
import gzip


root_dir = dirname(dirname(abspath(__file__)))
data_dir = '{}/data'.format(root_dir)

def test_all_proxy(timestamp, domain='proxydocker', nproc=8):

    json_in = '{}/{}.{}.proxies.json.gz'.format(data_dir, domain, timestamp)
    list_out = '{}/{}.{}.proxies.valid.list'.format(data_dir, domain, timestamp)
    data = json.loads(gzip.open(json_in).read().decode('utf-8'))

    proxy_list = sorted(list(data.keys()))
    print('validating {} proxies ...'.format(len(proxy_list)))
    # proxy_list = [x for x in range(100)]
    p = Pool(processes=nproc)
    r = [p.apply_async(test_proxy, args=(x,)) for x in proxy_list]
    output = [x.get() for x in r]
    output = [x for x in output if x != 'Null']

    print('writing ' + list_out, file=sys.stderr)
    fout = open(list_out, 'w')
    for proxy in output:
        print(proxy[0], proxy[1], sep='\t', file=fout)
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
                return proxy_url, 'PASS'
        except:
            pass

        nretry += 1
        time.sleep(1)

    return proxy_url, 'FAIL'


if __name__ == '__main__':

    timestamp = sys.argv[1]
    test_all_proxy(timestamp)
