import os
import json
import sys
from kit import utils
import requests
import time
from lxml import etree
from urllib.parse import urljoin


host = 'www.bioxbio.com'

def get_journal_links(in_url, tsleep):
    '''Get all journal links under input URL
    http://www.bioxbio.com/if/subject/{subject}-{n}.html
    '''

    data = {}
    error = None
    try:
        utils.qprint('get ' + in_url)
        r = requests.get(in_url)
        if not r.ok:
            raise
        time.sleep(tsleep)
        text = etree.HTML(r.text)
        for a in text.xpath('//tr/td/a'):
            title = a.text
            url = a.get('href')
            url = urljoin(in_url, url)
            data[url] = title

    except Exception as e:
        error = '*ERROR* ' + str(e)
        raise error
        data = {}

    return data, error


def get_subject_npage(subject):

    url = 'http://www.bioxbio.com/if/subject/{}-1.html'.format(subject)

    npage = 1
    error = None
    try:
        r = requests.get(url)
        if not r.ok:
            raise
        text = etree.HTML(r.text)
        for a in text.xpath('//li/a'):
            url  = a.get('href')
            if url.startswith(subject + '-') and url.endswith('.html'):
                page_num = int(a.text)
                if page_num > npage:
                    npage = page_num

    except Exception as e:
        error = '*ERROR* ' + str(e)
        npage = 0

    return npage, error



def get_all_journal_links(nproc=3, nretry=10, tsleep=1):

    subject_list = [
        'biology', 'medicine', 'agriculture', 'chemistry', 'geoscience',
        'astronomy', 'engineering', 'management', 'environmental', 'math',
        'physics', 'social',
    ]

    data = {}
    for subject in subject_list:
        npage, error = get_subject_npage(subject)
        args_list = []
        for page in range(1, npage+1):
            url = ('http://www.bioxbio.com/if/subject/{}-{}.html'
                   .format(subject, page))
            args_list.append([url, tsleep])
        tmp = utils.parallel_call(get_journal_links, args_list,
                                  nproc, nretry)
        data[subject] = {}
        for x in tmp:
            for k,v in x.items():
                data[subject][k] = v

        utils.qprint('get urls of {} journals of subject {}'
                     .format(len(data[subject]), subject))

    return data


if __name__ == '__main__':

    if len(sys.argv) != 2:
        timestamp = utils.get_timestamp()
    else:
        timestamp = sys.argv[1]

    subject_json = '../data/{}.subject.json'.format(timestamp)
    data = {}
    if os.path.isfile(subject_json):
        data = utils.load_json(subject_json)
    else:
        data = get_all_journal_links()
        utils.write_json(data, subject_json)

    # print(json.dumps(data, sort_keys=True, indent=2))



    # get_all_journal_links()
    # data, error = get_journal_links('http://www.bioxbio.com/if/subject/astronomy-1.html', 1)
    # print(json.dumps(data, sort_keys=True, indent=2))
    # print(error)
