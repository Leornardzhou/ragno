# -*- coding: utf-8 -*-

import os, sys, json
import requests, lxml, re
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

# -------------------------------------------------------------------------

def download_xml(url, out_dir):

    if '?page=' in url:
        page_id = url.split('=')[-1]
        url_base = url.split('//')[1].split('?')[0].replace('.xml', '')
        out_name = '{}/{}.page{}.xml'.format(out_dir, url_base, page_id)
    else:
        out_name = '{}/{}'.format(out_dir, url.split('//')[1])

    tmp_out_dir = os.path.dirname(out_name)
    os.makedirs(tmp_out_dir, exist_ok=True)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    r = requests.get(url, headers=headers)
    time.sleep(1)
    xml_set = set()
    res_list = re.findall(r'<loc>(.*?)</loc>', r.text)

    fout = qopen(out_name, 'w')
    for res in res_list:
        if res.endswith('.xml') or '.xml?page=' in res:
            xml_set.add(res)
        print(res, file=fout)
    fout.close()

    return xml_set


def get_all_xml():

    out_dir = '../data/xml'

    xml_todo = {
        "http://iopscience.iop.org/sitemap.xml",
    }
    xml_done = set()

    while len(xml_todo):
        tmp_xml_todo = set()
        for xml in xml_todo:
            tmp_xml_set = download_xml(xml, out_dir)
            xml_done.add(xml)
            for x in tmp_xml_set:
                if x not in xml_done:
                    tmp_xml_todo.add(x)
        xml_todo = tmp_xml_todo
        qprint('{} more xml to download.'.format(len(xml_todo)))


if __name__ == '__main__':

    get_all_xml()
    # download_xml('https://www.nature.com/sitemap.xml', '../data/xml')


# end
