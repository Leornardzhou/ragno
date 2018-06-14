# -*- coding: utf-8 -*-

import os, sys, json
import requests

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

    return json.loads(qopen(in_json).read())


def write_text(in_str, out_name):

    fout = qopen(out_name, 'w')
    print(in_str, file=fout)
    fout.close()


def read_text(in_name):

    return qopen(in_name).read()


# -------------------------------------------------------------------------

def get_page(in_cookie_json, in_url, out_html):

    cookies = read_json(in_cookie_json)

    try:
        s = requests.Session()
        for c in cookies:
            s.cookies.set(c['name'], c['value'])

        qprint('get {}'.format(in_url))
        r = s.get(in_url)

        write_text(r.text, out_html)

    except Exception as e:
        qprint('*ERROR* ' + str(e))

# -------------------------------------------------------------------------

if __name__ == '__main__':

    in_cookie_json, in_url, out_html = sys.argv[1:4]
    get_page(in_cookie_json, in_url, out_html)


# end
