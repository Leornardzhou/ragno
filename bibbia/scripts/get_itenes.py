'''This script downloads all htmls of Italian/English/Spanish Versions of Bible
from vatican.va/archive/bible/index_it.htm
'''

from os.path import abspath, dirname
import os
import sys
import requests
import re
import time


def get_html(url):
    '''Get the HTML of a URL and return the text string.'''

    r = requests.get(url)
    time.sleep(1)
    if not r.ok:
        print('*ERROR*: failed to retrieve html from ' + url)
        sys.exit(0)
    html = r.text
    r.close()

    return html


def save_html(html, fname):
    '''Save the HTML text in an output file.'''

    print('writing '+ fname, file=sys.stderr)
    f = open(fname, 'w')
    print(html, file=f)
    f.close()


def get_all_htmls(lang):
    '''Download all htmls of Bible in a given language.

    Output data will be saved in ../data/[lang]/*.HTM

    Args:
        lang (str):  italian, english, spanish
    '''

    work_dir = dirname(dirname(abspath(__file__)))

    url = {
        'italian': 'http://www.vatican.va/archive/ITA0001/_INDEX.HTM',
        'english': 'http://www.vatican.va/archive/ENG0839/_INDEX.HTM',
        'spanish': 'http://www.vatican.va/archive/ESL0506/_INDEX.HTM',
    }

    out_dir = '{}/data/{}'.format(work_dir, lang)
    os.makedirs(out_dir, exist_ok=True)

    index_html = get_html(url[lang])

    index = 0
    chpt_url_list = re.findall(r'<a href=(__P.*?)>', index_html)
    for chpt_url in chpt_url_list:
        fname = '{}/{}_{}'.format(out_dir, str(index).zfill(4), chpt_url)
        chpt_url = '{}/{}'.format(dirname(url[lang]), chpt_url)
        if not os.path.isfile(fname):
            html = get_html(chpt_url)
            save_html(html, fname)
        index += 1


if __name__ == '__main__':

    for lang in ['italian', 'english', 'spanish']:
        get_all_htmls(lang)
