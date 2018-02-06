from os.path import abspath, dirname
import os
import sys
import requests
import re


def get_html(url):

    r = requests.get(url)
    if not r.ok:
        print('*ERROR*: failed to retrieve html from ' +url[lang])
        sys.exit(0)

    return r.text


def save_html(html, fname):

    print('writing '+ fname, file=sys.stderr)
    f = open(fname, 'w')
    print(html, file=f)
    f.close()


def get_all_htmls(lang):

    work_dir = dirname(dirname(abspath(__file__)))

    url = {
        'italian': 'http://www.vatican.va/archive/ITA0001/_INDEX.HTM',
        'english': 'http://www.vatican.va/archive/ENG0839/_INDEX.HTM',
    }

    out_dir = '{}/data/{}'.format(work_dir, lang)
    os.makedirs(out_dir, exist_ok=True)

    index_html = get_html(url[lang])

    chpt_url_list = re.findall(r'<a href=(__P.*?)>', index_html)
    for chpt_url in chpt_url_list:
        fname = '{}/{}'.format(out_dir, chpt_url)
        chpt_url = '{}/{}'.format(dirname(url[lang]), chpt_url)
        html = get_html(chpt_url)
        save_html(html, fname)


if __name__ == '__main__':

    for lang in ['italian', 'english']:
        get_all_htmls(lang)
