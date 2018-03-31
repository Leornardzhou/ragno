'''This program scrapes all data at URL
http://chinahpo.org/

It takes as known list of OMIM/HPO IDs and scrape the translation.
'''

import os
from os.path import dirname, abspath
import requests
from kit import utils
from lxml import etree
import json
import time
import random

# use Chrome Dev Tools (Network) and inspect the requests send via
# http://chinahpo.org/database.html?search=100200&type=1&page=1

host = 'http://49.4.68.254:8081/knowledge'
token = 'Token 955290c5fbddd689e179fcd63dd4fe39b880b222'

def get_data(oid, out_json, proxy_set, tsleep):
    '''input Ontology ID, output in ../data
    '''

    if os.path.isfile(out_json):
        return None, None

    out_dir = abspath(dirname(out_json))
    os.makedirs(out_dir, exist_ok=True)

    proxies = None
    if len(proxy_set):
        proxy = random.choice(list(proxy_set))
        proxies = {'http': proxy}

    headers = {
        'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/39.0.2171.95 Safari/537.36'),
        'Authorization': token,
    }
    timeout_connect = 10
    timeout_read = 30
    timeout = (timeout_connect, timeout_read)

    # need to change
    url = None
    if oid.startswith('HP:'):
        url = host + '/hpo/?search={}&type=0&page=1'.format(oid)
    elif oid.startswith('OMIM:'):
        oid = oid.split(':')[1]
        url = host + '/omim/?search={}&type=1&page=1'.format(oid)
    else:
        raise 'input ID is not HP or OMIM'

    data = dict()
    error = None
    try:
        utils.qprint('get ' + url)
        r = requests.get(url, headers=headers, proxies=proxies, timeout=timeout)
        time.sleep(tsleep)
        if not r.ok:
            raise 'can not get url: ' + url

        data = json.loads(r.text)
        if len(data) != 4:
            raise 'output json seems incorrect (missing keys)'

        utils.write_json(data, out_json)

    except Exception as e:
        error = '*ERROR* ' + str(e)
        data = dict()
        # print(error)
        # raise

    return None, error


def get_all_data(in_oid_list, out_dir, nproc=3, nretry=10, tsleep=1,
                 proxy_list=None):

    # load proxy
    proxy_set = set()
    if os.path.isfile(proxy_list):
        for line in open(proxy_list):
            proxy_set.add(line.rstrip().split('\t')[0])

    # load oid list
    oid_list = []
    for line in open(in_oid_list):
        oid = line.rstrip()
        oid_list.append(oid)

    oid_list = oid_list
    args_list = []
    for oid in oid_list:
        oid_name = oid.replace(':', '.').lower()
        out_json = '{}/{}.json.gz'.format(out_dir, oid_name)
        args_list.append([oid, out_json, proxy_set, tsleep])

    data = utils.parallel_call(get_data, args_list, nproc, nretry)


if __name__ == '__main__':

    dt = utils.DTime()

    out_json = '../data/short_list/omim_diseases.json'
    # data, error = get_data('OMIM:100200', 'OMIM.100200.json')
    # print(data)
    # print(error)

    in_oid_list = '../input/oid.list'
    out_dir = '../data/full_data'
    proxy_list = 'proxy.list'
    get_all_data(in_oid_list, out_dir, nproc=8, nretry=100, tsleep=5,
                 proxy_list=proxy_list)

    dt.diff_time()
