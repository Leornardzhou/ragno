'''This script downloads all pdfs of Traditional Chinese Version of Bible from
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
    '''Download all PDFs of Bible in Traiditional Chinese.

    '''

    work_dir = dirname(dirname(abspath(__file__)))
    out_dir = '{}/data/chinese_tw'.format(work_dir)
    os.makedirs(out_dir, exist_ok=True)

    url = 'http://www.vatican.va/chinese/bibbia.htm'
    r = requests.get(url)
    pdf_list = re.findall(r'href="(.*?)">', r.text)
    r.close()

    uniq_pdf_list = []
    for pdf in pdf_list:
        if pdf not in uniq_pdf_list:
            uniq_pdf_list.append(pdf)

    for i, pdf in enumerate(uniq_pdf_list):
        pdf_url = 'http://www.vatican.va/chinese/' + pdf
        foo, part, title = pdf.split('/')[:3]
        fname = '{}/{}_{}_{}'.format(out_dir, str(i).zfill(3), part, title)
        save_pdf(pdf_url, fname)
        print('converting pdf {} to text ...'.format(fname))
        os.system('pdftotext '+fname)


if __name__ == '__main__':

    get_all_pdfs()
