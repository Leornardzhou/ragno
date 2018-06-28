# -*- coding: utf-8 -*-

import os, sys, json, gzip
import re
from lxml import etree

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

def show_content(in_html_gz):

    text = read_text(in_html_gz, verbose=False)
    root = etree.HTML(text)
    content = root.xpath('//div[@property="schema:articleBody"]')
    for x in content:
        print(''.join(x.itertext()))






if __name__ == '__main__':

    in_html_gz = sys.argv[1]
    show_content(in_html_gz)


# end
