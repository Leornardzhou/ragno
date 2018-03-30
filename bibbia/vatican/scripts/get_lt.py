'''This script downloads all htmls of Latin Versions of Bible
from http://www.vatican.va/archive/bible/nova_vulgata/documents/nova-vulgata_index_lt.html
'''

from os.path import abspath, dirname
import os
import sys
import requests
import re
import time

host = 'http://www.vatican.va/archive/bible/nova_vulgata/documents'
work_dir = dirname(dirname(abspath(__file__)))

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


def get_other_htmls():
    '''Download preface and appendix htmls of Bible in Latin.

    Output data will be saved in ../data/latin/others/*.html
    '''

    out_dir = '{}/data/latin/others'.format(work_dir)
    os.makedirs(out_dir, exist_ok=True)

    urls = {
        'Constitutio Apostolica': host + '/nova-vulgata_jp-ii_apost_const_lt.html',
        'Praefatio ad Lectorem': host + '/nova-vulgata_praefatio_lt.html',
        'Praenotanda': host + '/nova-vulgata_praenotanda_lt.html',
        'Appendix Decretum de Canonicis Scripturis': host + '/nova-vulgata_appendix_decretum-can-script_lt.html',
        'Appendix Decretum de editione et usu Sacrorum Librorum': host + '/nova-vulgata_appendix_decr-editione-usu_lt.html',
        'Praefatio ad Lectorem (trium editionum Clementinarum)': host + '/nova-vulgata_appendix_praefatio-lectorem_lt.html',
    }

    for section,url in urls.items():
        fname = out_dir + '/' + url.split('/')[-1]
        html = get_html(url)
        save_html(html, fname)


def get_main_htmls():
    '''Download main htmls of Bible in Latin.

    Output data will be saved in ../data/latin
    '''

    out_dir = '{}/data/latin'.format(work_dir)
    os.makedirs(out_dir, exist_ok=True)

    urls = {
        'VETUS TESTAMENTUM': host + '/nova-vulgata_vetus-testamentum_lt.html',
        'NOVUM TESTAMENTUM': host + '/nova-vulgata_novum-testamentum_lt.html',
    }

    index = 0
    for section in ['VETUS TESTAMENTUM', 'NOVUM TESTAMENTUM']:
        url = urls[section]
        index_html = get_html(url)
        chpt_url_list = re.findall(r'<a href="(.*?)">', index_html)
        for chpt_url in chpt_url_list:
            if chpt_url == '#top':
                continue
            fname = '{}/{}_{}'.format(out_dir, str(index).zfill(3), chpt_url)
            chpt_url = '{}/{}'.format(host, chpt_url)
            html = get_html(chpt_url)
            save_html(html, fname)
            index += 1



if __name__ == '__main__':

    get_main_htmls()
    get_other_htmls()
