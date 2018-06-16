# -*- coding: utf-8 -*-

import os, sys, json
import requests, re
import datetime
import time

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


def write_text(in_str, out_text):

    fout = qopen(out_text, 'w')
    print(in_str, file=fout)
    fout.close()


def read_text(in_text):

    out_str = qopen(in_text).read()
    return out_str


def add_timestamp(fname, time_format="%Y%m%d%H"):

    time_stamp = datetime.datetime.now().strftime(time_format)
    fname_list = fname.rsplit('.', 1)
    new_fname = '{}.{}.{}'.format(fname_list[0], time_stamp, fname_list[1])
    return new_fname

# -------------------------------------------------------------------------

def get_sitemap(out_name):

    out_name = add_timestamp(out_name)
    out_dir = os.path.dirname(out_name)
    os.makedirs(out_dir, exist_ok=True)

    url = 'https://www.genomeweb.com/sitemap.xml'

    qprint('getting {}'.format(url))
    res = requests.get(url)

    loc_list = re.findall(r'<loc>(.*?)</loc>', res.text)
    fout = qopen(out_name, 'w')
    for loc in loc_list:
        qprint('getting {}'.format(loc))
        r = requests.get(loc)
        print(r.text, file=fout)
    fout.close()

# -------------------------------------------------------------------------

def process_sitemap(in_sitemap_name, in_pubpri_name,
                    out_failed_name, out_pubpri_name, out_pub_dir, time_sleep=1):
    '''
    Download all links in sitemap, distinguish if the page is public or
    privdate (mark them in the output list)
    '''

    # timestamp in output files
    out_failed_name = add_timestamp(out_failed_name)
    out_pubpri_name = add_timestamp(out_pubpri_name)

    # load in_pubpri_name
    url_dict = dict()
    if in_pubpri_name:
        for line in qopen(in_pubpri_name):
            url, mark = line.rstrip().split(',')
            url_dict[url] = mark

    fout_failed = qopen(out_failed_name, 'w')
    fout = qopen(out_pubpri_name, 'w')
    os.makedirs(out_pub_dir, exist_ok=True)
    for line in qopen(in_sitemap_name):
        if not line.startswith('<url>'):
            continue
        url_list = re.findall(r'<loc>(.*?)</loc>', line.rstrip())
        if url_list == 0:
            continue
        url = url_list[0]
        if url in url_dict or url.endswith('/'):
            continue

        qprint('getting {}'.format(url))
        res = requests.get(url)
        time.sleep(time_sleep)

        if not res.ok:
            print(line.rstrip(), file=fout_failed, flush=True)

        if 'paywall-box' in res.text:
            mark = 'private'
        else:
            mark = 'public'
        print(url, mark, sep=',', file=fout, flush=True)

        if mark == 'private':
            continue

        out_html = '{}/{}.html'.format(out_pub_dir, url.split('//')[1])
        if os.path.isfile(out_html):
            continue
        out_html_dir = os.path.dirname(out_html)
        os.makedirs(out_html_dir, exist_ok=True)
        write_text(res.text, out_html)

    fout_failed.close()
    fout.close()



# -------------------------------------------------------------------------
# -------------------------------------------------------------------------
# -------------------------------------------------------------------------

def process():

    pass




if __name__ == '__main__':

    # get_sitemap('../data/sitemap/sitemap.xml')
    process_sitemap('../data/sitemap/sitemap.2018061602.xml', False,
                    'failed.list', 'mark.list', '../data/html/public')


# end
