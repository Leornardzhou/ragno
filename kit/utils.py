'''This module contains common programs used in scraping.

TODO:
- Logging
'''

import sys
import gzip
import json
import multiprocessing
import datetime
import time

# -------------------------------------------------------------------------

def write_html(text, html_name, verbose=True):

    if verbose:
        qprint('write ' + html_name)
    if html_name.endswith('.gz'):
        fout = gzip.open(html_name, 'wb')
        fout.write((text+'\n').encode('utf-8'))
    else:
        fout = open(html_name, 'w')
        fout.write(text+'\n')
    fout.close()

# -------------------------------------------------------------------------

def load_html(html_name, verbose=True):

    if verbose:
        qprint('read ' + html_name)
    if html_name.endswith('.gz'):
        text = gzip.open(html_name).read().decode('utf-8')
    else:
        text = open(html_name).read()
    return text

# -------------------------------------------------------------------------

def get_timestamp(fmt_str="%Y%m%d%H%M"):
    timestamp = datetime.datetime.now().strftime(fmt_str)
    return timestamp

# -------------------------------------------------------------------------

def qprint(msg, verbose=True):
    print(':: ' + msg, file=sys.stderr, flush=True)

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

def load_json(json_name, verbose=True):
    if verbose:
        qprint('read ' + json_name)
    if json_name.endswith('.gz'):
        data = json.loads(gzip.open(json_name).read().decode('utf-8'))
    else:
        data = json.loads(open(json_name).read())
    return data

# -------------------------------------------------------------------------

def parallel_call(callback_func, args_list, nproc=8, nretry=10,
                  verbose=True):
    '''
    callback_func returns [True/False, string of errors caught]
    '''
    njob = len(args_list)
    i = 0
    data = []
    while len(args_list) and i < nretry:
        # get all contents
        if verbose:
            qprint('retry: {} (njob={})'.format(i, len(args_list)))
        pool = multiprocessing.Pool(processes=nproc)
        res = []
        for args in args_list:
            res.append(pool.apply_async(callback_func, args))
        tmp = [x.get() for x in res]
        # filter results
        args_list = [x for x,t in zip(args_list, tmp) if t[1]]
        data.extend([t[0] for t in tmp if not t[1]])
        pool.close()
        pool.join()
        i += 1

    nleft = len(args_list)
    if nleft:
        qprint('*ERROR* maximum {} retries reached, {}/{} jobs unfinished.'
               .format(nretry, nleft, njob))
    return data

# -------------------------------------------------------------------------

class DTime(object):

    def __init__(self):
        self.tcheck = time.time()

    def diff_time(self, msg=''):
        t = time.time()
        dt = t - self.tcheck
        self.tcheck = t
        unit = 'seconds'
        if dt > 60:
            dt /= 60
            unit = 'minutes'
        if msg:
            qprint('"{}" is DONE in {} {}'.format(msg, round(dt,2), unit))
        else:
            qprint('DONE in {} {}'.format(round(dt,2), unit))
