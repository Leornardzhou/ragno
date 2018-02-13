'''This script downloads all htmls of Chinese Simplified Versions of Bible
from http://xiaozhushou.org/index.php/?m=bible&template=12&chapter=24
'''

from os.path import abspath, dirname
import os
import sys
import requests
import re
import time
import utils


host = 'http://www.vatican.va/archive/bible/nova_vulgata/documents'
work_dir = dirname(dirname(abspath(__file__)))

def get_content(driver, chpt_url, out_html_name, out_audio_name):

    utils.open_url(driver, chpt_url, verbose=True)
    elem = driver.find_element_by_xpath('//div[@id="bible_chapter_content"]')
    save_html(elem.get_attribute('outerHTML'), out_html_name)
    try:
        audio_url = driver.find_element_by_xpath('//audio').get_attribute('src')
        utils.download_file(audio_url, out_audio_name)
    except:
        pass


def save_html(html, fname):
    '''Save the HTML text in an output file.'''

    print('writing '+ fname, file=sys.stderr)
    f = open(fname, 'w')
    print(html, file=f)
    f.close()


def get_all_htmls():
    '''Download all htmls of Bible in Chinese.

    Output data will be saved in ../data/chinese_cn/*.html
    '''

    driver = utils.start_driver('phantomjs', verbose=True)
    out_dir = '{}/data/chinese_cn'.format(work_dir)
    os.makedirs(out_dir, exist_ok=True)

    try:
        for i in range(1, 74):
            url = ('http://xiaozhushou.org/index.php/?m=bible&template={}'
                   .format(i))
            utils.open_url(driver, url, verbose=True)
            chpt_url_list = []
            for elem in driver.find_elements_by_xpath(
                    '//ul[@id="chapter_list"]/li/a'):
                chpt_url = elem.get_attribute('href')
                chpt_url_list.append(chpt_url)

            for chpt_url in chpt_url_list:
                book_id = str(i).zfill(3)
                chpt_id = chpt_url.split('=')[-1].zfill(3)
                out_html_name = ('{}/{}_{}_chapter.html'
                                 .format(out_dir, book_id, chpt_id))
                out_audio_name = ('{}/{}_{}_audio.mp3'
                                 .format(out_dir, book_id, chpt_id))
                get_content(driver, chpt_url, out_html_name, out_audio_name)

    except:
        print('*ERROR* something wrong')
        raise

    finally:
        utils.close_driver(driver, verbose=True)


if __name__ == '__main__':

    get_all_htmls()
