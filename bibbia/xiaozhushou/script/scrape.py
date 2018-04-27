import os
import sys
import json
import requests
import time
from lxml import etree
import re

from kit import utils


host = 'https://www.xiaozhushou.org'

def get_chapter_text(in_url, out_json, tsleep):

    data = {}
    error = None

    if os.path.isfile(out_json):
        return data, error

    try:
        utils.qprint('get ' + in_url)
        r = requests.get(in_url)
        if not r.ok:
            raise Exception('can not get url ' + in_url)
        time.sleep(tsleep)
        text = etree.HTML(r.text)

        data['url'] = in_url

        pattern = (r'<span class="chapter_title"> (.*?) <i class="glyphicon '
                   'glyphicon-chevron-right "> </i> (.*?) <i class="glyphicon '
                   'glyphicon-chevron-right"> </i> (.*?)</span>')
        x = re.findall(pattern, r.text)
        if x:
            data['volume'] = x[0][0]
            data['book'] = x[0][1]
            data['chapter'] = x[0][2]
        else:
            data['volume'] = None
            data['book'] = None
            data['chapter'] = None

        phrase_set = set()
        data['content'] = []
        for x in text.xpath('//div[@id="bible_chapter_content"]/*'):
            t = {'vers': None, 'text': None}
            if x.tag == 'p':
                t = {'vers': x.get('value'), 'text': x.text.split('  ', 1)[-1]}
            else:
                t = {'vers': '', 'text': x.text}
            if t['vers'] == None and t['text'] == None:
                raise Exception('can not extract content from "{}" (url={})'
                                .format(x.text, in_url))
            # avoid duplicate entry
            phrase = '|{}|{}|'.format(t['vers'], t['text'])
            if phrase not in phrase_set:
                data['content'].append(t)
                phrase_set.add(phrase)

        utils.write_json(data, out_json)
        data = {}

    except Exception as e:
        error = '*ERROR* ' + str(e)
        raise
        data = {}

    return data, error


def get_chapter_links(in_url, tsleep):

    data = []
    error = None

    try:
        utils.qprint('get ' + in_url)
        r = requests.get(in_url)
        if not r.ok:
            raise Exception('can not get url ' + in_url)
        time.sleep(tsleep)

        p = (r'<a href="/index.php/\?m=bible&template=(.*?)&chapter=(.*?)"  '
             '>(.*?)</a>')
        for x in re.findall(p, r.text):
            book, chapter, title = x
            url = ('{}/index.php/?m=bible&template={}&chapter={}'
                   .format(host, book, chapter))
            out = {
                'book': book,
                'chapter': chapter,
                'title': title,
                'url': url,
            }
            data.append(out)

    except Exception as e:
        error = '*ERROR* ' + str(e)
        data = []
        raise

    return data, error


def get_all_chapter_text(link_data, out_dir, tsleep=1, nproc=3, nretry=10):

    os.makedirs(out_dir, exist_ok=True)
    args_list = []
    for x in link_data:
        in_url = x['url']
        out_json = '{}/book{}.chapter{}.json'.format(out_dir, x['book'],
                                                     x['chapter'])
        args_list.append([in_url, out_json, tsleep])

    utils.parallel_call(get_chapter_text, args_list, nproc=nproc, nretry=nretry)


def get_all_chapter_links(out_json, tsleep=1, nproc=3, nretry=10):

    data = []
    args_list = []
    for i in range(1, 74):
        url = '{}/index.php/?m=bible&template={}'.format(host, i)
        args_list.append([url, tsleep])
    tmp = utils.parallel_call(get_chapter_links, args_list,
                              nproc=nproc, nretry=nretry)
    for x in tmp:
        for y in x:
            data.append(y)

    utils.write_json(data, out_json)
    return data


def test():

    # in_url = 'https://www.xiaozhushou.org/index.php/?m=bible&template=23&chapter=0'
    in_url = 'https://www.xiaozhushou.org/index.php/?m=bible&template=26&chapter=3'
    out_json = 'foo.json'
    tsleep = 0

    data, error = get_chapter_text(in_url, out_json, tsleep)
    # data, error = get_chapter_links(in_url, tsleep)

    print(json.dumps(data, sort_keys=True, ensure_ascii=False, indent=2))
    print(error)


def scrape():

    if len(sys.argv) == 2:
        ts = sys.argv[1]
    else:
        ts = utils.get_timestamp()

    out_dir = '../data'
    os.makedirs(out_dir, exist_ok=True)

    link_json = '{}/{}.links.json'.format(out_dir, ts)
    link_data = {}
    if os.path.isfile(link_json):
        link_data = utils.load_json(link_json)
    else:
        link_data = get_all_chapter_links(link_json)

    get_all_chapter_text(link_data, '{}/{}'.format(out_dir, ts))


if __name__ == '__main__':

    # test()
    scrape()
