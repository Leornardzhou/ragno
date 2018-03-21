'''This program retrieves data via steamspy.com/api.php


http://steamspy.com/api.php?request=top100in2weeks
http://steamspy.com/api.php?request=top100forever
http://steamspy.com/api.php?request=top100owned
http://steamspy.com/api.php?request=all

steamspy.com/api.php?request=appdetails&appid=730

steamspy.com/api.php?request=tag&tag=Bowling

steamspy.com/api.php?request=genre&genre=Early+Access

'''

import os
import sys
import requests
import time
import json
import random
import multiprocessing
import datetime
import gzip

host = 'http://steamspy.com/api.php'


def write_json(data, fname):
    '''Write compressed/uncompressed JSON file.'''

    print(': writing ' + fname, file=sys.stderr, flush=True)
    if fname.endswith('.gz'):
        fout = gziop.open(fname, 'wb')
        fout.write(json.dumps(data, sort_keys=True).encode('utf-8'))
    else:
        fout = open(fname, 'w')
        print(json.dumps(data, sort_keys=True), file=fout)
    fout.close()


def load_json(fname):
    '''Read compressed/uncompressed JSON file.'''

    print(': reading ' + fname, file=sys.stderr, flush=True)
    if fname.endswith('.gz'):
        return json.loads(gzip.open(fname).read().decode('utf-8'))
    else:
        return json.loads(open(fname).read())


def load_proxy_list(proxy_dir):
    '''Load a list of validated proxies.'''

    proxy_set = set()
    for fname in os.listdir(proxy_dir):
        if not fname.endswith('.validated.list.gz'):
            continue
        fname = proxy_dir + '/' + fname
        print(': readng ' + fname)
        if fname.endswith('.gz'):
            for line in gzip.open(fname):
                proxy, npass, nfail, etime = line.decode('utf-8').rstrip().split('\t')
                if npass == '0':
                    continue
                proxy_set.add(proxy)
        else:
            for line in open(fname):
                proxy, npass, nfail, etime = line.rstrip().split('\t')
                if npass == '0':
                    continue
                proxy_set.add(proxy)

    print(': loaded {} validated proxies'.format(len(proxy_set)),
          file=sys.stderr)

    return sorted(list(proxy_set))


def generate_genre_url_dict():

    genre_set = {
        'Free', 'Massively', 'Ex+Early+Access', 'Early+Access', 'Simulation',
        'Sports', 'Adventure', 'Indie', 'RPG', 'Strategy', 'Action',
    }
    url_dict = dict()
    for genre in genre_set:
        url_dict[genre] = ('http://steamspy.com/api.php?request=genre&genre={}'
                           .format(genre))

    return url_dict


def generate_top_url_dict():

    top_set = {
        'top100in2weeks', 'top100forever', 'top100owned', 'all',
    }
    url_dict = dict()
    for key in top_set:
        url_dict[key] = ('http://steamspy.com/api.php?request={}'
                         .format(key))
    return url_dict


def generate_app_url_dict(all_json):

    appid_list = list(load_json(all_json))
    url_dict = dict()
    for key in appid_list:
        url_dict[key] = (
            'http://steamspy.com/api.php?request=appdetails&appid={}'
            .format(key))
    return url_dict


def generate_tag_url_dict(app_dir):

    tag_set = set()
    for fname in os.listdir(app_dir):
        fname = app_dir + '/' + fname
        data = json.loads(open(fname).read())
        for tag in data['tags']:
            tag_set.add(tag.replace(' ', '+'))

    url_dict = dict()
    for key in tag_set:
        url_dict[key] = (
            'http://steamspy.com/api.php?request=tag&tag={}'.format(key))
    return url_dict


def get_all_urls(proxy_list, url_dict, out_dir,
                 nproc=8, overwrite=False, timeout_connect=10,
                 timeout_read=30, timesleep=1):
    '''call query() to retrieve all urls in url_dict and save each as json'''

    os.makedirs(out_dir, exist_ok=True)

    url_dict = {k:url_dict[k] for k in list(url_dict)}

    data = dict()
    nretry = 1000
    for i in range(nretry):
        print(': {} urls to retrieve (retry={})'.format(len(url_dict), i),
              file=sys.stderr, flush=True)

        pool = multiprocessing.Pool(processes=nproc)
        res = []
        for key, url in sorted(url_dict.items()):
            out_json = '{}/{}.json'.format(out_dir, key)
            res.append(pool.apply_async(
                query,
                (url, proxy_list, out_json, overwrite, timeout_connect,
                 timeout_read, timesleep)))
        pool.close()
        pool.join()

        done_set = set()
        for key, url in sorted(url_dict.items()):
            out_json = '{}/{}.json'.format(out_dir, key)
            if os.path.isfile(out_json):
                done_set.add(key)
                url_dict.pop(key)

        if len(url_dict) == 0:
            break



def query(url, proxy_list, out_json, overwrite, timeout_connect, timeout_read,
          timesleep):
    '''query api without retry'''

    if os.path.isfile(out_json) and not overwrite:
        return

    proxy = random.choice(proxy_list)
    data = dict()
    proc = multiprocessing.current_process()

    try:
        print(':: get {} proxy={} ({}, {})'
              .format(url, proxy, proc.name, proc.pid), file=sys.stderr,
              flush=True)
        time.sleep(timesleep)
        r = requests.get(url, proxies={'http':proxy},
                         timeout=(timeout_connect, timeout_read))
        data = json.loads(r.text)
        if data or r.text.startswith('{}'):
            write_json(data, out_json)
    except:
        pass
    # except Exception as e:
    #     print('*ERROR*: proxy={} url={} {}'.format(proxy, url, str(e)),
    #           file=sys.stderr, flush=True)




if __name__ == '__main__':


    # proxy_dir = '../../proxy/data_valid/'
    # out_dir = 'test20180319'

    tstart = time.time()

    proxy_dir, out_dir = sys.argv[1:3]
    proxy_list = load_proxy_list(proxy_dir)

    print('----- retieve all/top games -----', file=sys.stderr, flush=True)
    url_dict = generate_top_url_dict()
    get_all_urls(proxy_list, url_dict, out_dir+'/top')

    print('----- retieve game genres -----', file=sys.stderr, flush=True)
    url_dict = generate_genre_url_dict()
    get_all_urls(proxy_list, url_dict, out_dir+'/genre')

    print('----- retieve game details -----', file=sys.stderr, flush=True)
    url_dict = generate_app_url_dict(out_dir+'/top/all.json')
    get_all_urls(proxy_list, url_dict, out_dir+'/app')

    print('----- retieve game tags -----', file=sys.stderr, flush=True)
    url_dict = generate_tag_url_dict(out_dir+'/app')
    get_all_urls(proxy_list, url_dict, out_dir+'/tag')

    tend = time.time()

    print('----- DONE in {0:.2f} minutes -----'.format((tend-tstart)/60),
          file=sys.stderr, flush=True)
