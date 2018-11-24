# -*- coding: utf-8 -*-

import os, sys, json, gzip, time
import re, requests

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

def down_list(todo_list, cookie_name, data_dir, sleep_time=2.5):

    # load cookie
    cookies = read_json(cookie_name)
    s = requests.Session()
    for c in cookies:
        s.cookies.set(c['name'], c['value'])

    todo_set = set(read_text(todo_list).rstrip().split('\n'))
    todo_set = {x for x in todo_set if x.startswith('https://')}
    qprint('found {} urls in todo list {}'.format(len(todo_set), todo_list))

    niter = 0
    niter_max = 20
    while len(todo_set) and niter < niter_max:

        failed_set = set()
        qprint('iteration-{}: {} urls to extract'.format(niter, len(todo_set)))

        for url in sorted(todo_set):
            url_base = re.sub(r'https://www.genomeweb.com/', '', url)
            out_name = '{}/{}.html'.format(data_dir, url_base)
            if os.path.isfile(out_name + '.gz'):
                continue
            tmp_out_dir = os.path.dirname(out_name)
            os.makedirs(tmp_out_dir, exist_ok=True)

            try:
                r = s.get(url)
                time.sleep(sleep_time)

                if 'paywall-box' in r.text:
                    qprint('*ERROR* paywall-box found in {}, time to renew '
                           'cookies.'.format(url))
                    sys.exit(0)

                write_text(r.text, out_name + '.gz')

            except Exception as e:
                qprint('*ERROR* failed to retrieve {}'.format(url))
                failed_set.add(url)

        todo_set = failed_set
        niter += 1


if __name__ == '__main__':


    cwd = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.abspath(os.path.join(cwd, '../data'))

    # todo_list = '../data/sitemap/url_todo_2018062814.list.gz'
    timestamp = sys.argv[1]
    todo_list = '../data/sitemap/url_todo_{}.list.gz'.format(timestamp)
    cookie_name = 'cookies/cookies.genomeweb.2018061522.json'
    down_dir = '{}/html/www.genomeweb.com'.format(data_dir)
    down_list(todo_list, cookie_name, down_dir)


# end
