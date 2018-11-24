# -*- coding: utf-8 -*-

import os, sys, json, gzip
import re, requests
import datetime

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
        if mode == 'w':
            qprint('writing {}'.format(fname))
        else:
            qprint('reading {}'.format(fname))

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

def find_downloaded(down_dir, out_list=False):
    '''
    down_dir = path/to/www.genomeweb.com
    '''

    qprint('checking files downloaded in {}'.format(down_dir))
    url_set = set()
    for root, dirs, files in os.walk(down_dir):
        if 'www.genomeweb.com' not in root:
            continue
        for f in files:
            if not f.endswith('html.gz'):
                continue
            f = os.path.join(root, f)
            url = re.sub(r'(.*?)www.genomeweb.com/','www.genomeweb.com/', f)
            url = re.sub(r'.html.gz$', '', url)
            url_set.add('https://' + url)

    qprint('found {} downloaded urls'.format(len(url_set)))

    if out_list:
        fout = qopen(out_list, 'w')
        for url in sorted(url_set):
            print(url, file=fout)
        fout.close()

    return url_set

# -------------------------------------------------------------------------

def get_sitemap(out_list=False):

    url = 'https://www.genomeweb.com/sitemap.xml'
    qprint('get url {}'.format(url))
    res = requests.get(url)
    loc_list = re.findall(r'<loc>(.*?)</loc>', res.text)

    url_set = set()
    for url_xml in loc_list:
        qprint('get url {}'.format(url_xml))
        res = requests.get(url_xml)
        for line in res.text.split('\n'):
            if line.startswith('<url>'):
                url_page = re.findall(r'<loc>(.*?)</loc>', line)[0]
                url_set.add(url_page)

    qprint('found {} urls from sitemap'.format(len(url_set)))

    if out_list:
        fout = qopen(out_list, 'w')
        for url in sorted(url_set):
            print(url, file=fout)
        fout.close()

    return url_set

# -------------------------------------------------------------------------

def create_todo(url_all, url_done, out_list=False):

    url_todo = url_all - url_done
    url_todo -= {'https://www.genomeweb.com/'}

    qprint('found {} urls to download'.format(len(url_todo)))

    if out_list:
        write_text('\n'.join(sorted(url_todo)), out_list)

    return url_todo


# -------------------------------------------------------------------------

def create_list(data_dir, todo_list):

    url_done = find_downloaded(data_dir)
    url_all = get_sitemap()
    create_todo(url_all, url_done, todo_list)

# -------------------------------------------------------------------------

if __name__ == '__main__':

    cwd = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.abspath(os.path.join(cwd, '../data'))

    if len(sys.argv) == 1:
        timestamp = get_timestamp(fmt_str="%Y%m%d%H")
    else:
        timestamp = sys.argv[1]
    down_dir = '{}/html/www.genomeweb.com'.format(data_dir)
    todo_list = '{}/sitemap/url_todo_{}.list.gz'.format(data_dir, timestamp)
    create_list(down_dir, todo_list)


# end
