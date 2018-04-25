import os
import sys
import json
import requests
import time
from lxml import etree
import re
import html

from kit import utils


host = 'http://www.bibbiaedu.it'

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
        x = text.xpath('//div[@class="libro"]')
        data['book'] = x[0].text if x else None

        x = text.xpath('//div[@id="capitolo"]')
        data['chapter'] = x[0].text.strip() if x else None

        data['content'] = []
        el = text.xpath('//div[@class="testidellibro"]')[0]
        s = html.unescape(etree.tostring(el).decode('utf-8'))
        for line in s.split('\n'):
            if not line.startswith('<sup>'):
                continue
            x = re.findall(r'<sup><a class="numversetto" id="(.*?)" '
                           'name="(.*?)">(.*?)</a></sup>(.*?)$', line)
            if not x:
                continue
            foo, foo, vers, phrase = x[0]
            phrase = re.sub(r'<.*?>', ' ', phrase)
            phrase = re.sub(r'\t', ' ', phrase)
            phrase = re.sub(r' +', ' ', phrase)
            t = {'vers': vers, 'text': phrase.strip()}
            data['content'].append(t)

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

        book = re.findall('&idlibroz=(.*?)$', in_url)[0]
        p = (r'<a id="ext" href="(.*?)" alt="altri capitoli del '
             'libro">(.*?)</a>')

        for x in re.findall(p, r.text):
            url, chapter = x
            y = re.findall(r'Libro=(.*?)&capitolo=(.*?)&', url)
            title, chapter = y[0]
            url = host + url
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
        url = ('{}/pls/labibbia_new/Bibbia_Utils.elenco_capitoli?'
               'origine=cei2008&idlibroz={}'.format(host, i))
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
    # in_url = 'https://www.xiaozhushou.org/index.php/?m=bible&template=16&chapter=0'
    # in_url = 'http://www.bibbiaedu.it/testi/Bibbia_CEI_2008.Ricerca?Libro=Genesi&capitolo=3&visintro=0&idp=1'
    in_url = 'http://www.bibbiaedu.it/testi/Bibbia_CEI_2008.Ricerca?Libro=Salmi&capitolo=26&idp=3'
    in_url = 'http://www.bibbiaedu.it/testi/Bibbia_CEI_2008.Ricerca?Libro=1%20Re&capitolo=13&visintro=1&idp=2'

    in_url = 'http://www.bibbiaedu.it/pls/labibbia_new/Bibbia_Utils.elenco_capitoli?origine=cei2008&idlibroz=32'
    out_json = 'foo.json'
    tsleep = 0

    # data, error = get_chapter_text(in_url, out_json, tsleep)
    data, error = get_chapter_links(in_url, tsleep)

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
