'''This script downloads all pdfs of Chinese Version of Bible from
http://www.vatican.va/chinese/bibbia.htm '''

import os
from os.path import abspath, dirname
import sys
import requests
import re


def save_pdf(url, fname, chunk_size=1024):
    '''Save the PDF in an output file.'''

    r = requests.get(url, stream=True)
    print('saving {} to {}'.format(url, fname), file=sys.stderr)
    with open(fname, 'wb') as f:
        for chunk in r.iter_content(chunk_size=chunk_size):
            if chunk:
                f.write(chunk)
    r.close()


def get_all_pdfs():
    '''Download all PDFs of Bible in Chinese.

    '''

    work_dir = dirname(dirname(abspath(__file__)))
    out_dir = '{}/data/chinese'.format(work_dir)
    os.makedirs(out_dir, exist_ok=True)

    url = 'http://www.vatican.va/chinese/bibbia.htm'
    r = requests.get(url)
    pdf_list = re.findall(r'href="(.*?)">', r.text)
    r.close()

    for i, pdf in enumerate(pdf_list):
        pdf_url = 'http://www.vatican.va/chinese/' + pdf
        foo, part, title = pdf.split('/')[:3]
        fname = '{}/{}_{}'.format(out_dir, part, title)
        save_pdf(pdf_url, fname)


if __name__ == '__main__':
    get_all_pdfs()
