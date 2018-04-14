import os
import json
import sys
from kit import utils
import requests
import time
from lxml import etree
from urllib.parse import urljoin
import re


host = 'www.bioxbio.com'

def get_journal_data(in_url, out_json, tsleep):
    '''Get journal data (name, issn, impact factors) from input URL
    http://www.bioxbio.com/if/html/{journal}.html
    '''

    data = {}
    error = None

    if os.path.isfile(out_json):
        return data, error

    try:
        utils.qprint('get ' + in_url)
        r = requests.get(in_url)
        if not r.ok:
            raise
        time.sleep(tsleep)

        root = etree.HTML(r.text)

        data['url'] = in_url
        data['title'] = root.xpath('//div/h1')[0].text
        x = re.findall(r'<p>Journal Abbreviation: (.*?)<br>', r.text)
        data['title_abbrev'] = x[0] if x else x
        x = re.findall(r'Journal ISSN: (.*?)</p>', r.text)
        data['issn'] = x[0] if x else x

        data['impact'] = {}
        for tr in root.xpath('//table/tr'):
            td_list = tr.xpath('./td')
            if len(td_list) != 3:
                continue
            year, ifact, npub = [x.text for x in td_list]
            if year == 'Year':
                continue
            try:
                ifact = float(ifact)
            except:
                ifact = -1
            try:
                npub = int(npub)
            except:
                npub = -1
            data['impact'][year] = {
                'ifact': ifact, 'npub': npub,
            }

        utils.write_json(data, out_json)

    except Exception as e:
        error = '*ERROR* ' + str(e)
        data = {}

    return data, error


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
        raise
        data = {}

    return data, error


def get_subject_npage(subject):
    '''Get maximum number of pages for each subject'''

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
    '''Get urls of all journals'''

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


def get_all_journal_data(all_journal_dict, out_dir,
                         nproc=3, nretry=10, tsleep=1):
    '''Get data of all journals'''

    os.makedirs(out_dir, exist_ok=True)

    args_list = []
    for subject in sorted(all_journal_dict):
        for url in sorted(all_journal_dict[subject]):
            journal_abbrev = re.findall(r'/if/html/(.*?).html', url)[0].lower()
            out_json = '{}/{}.json'.format(out_dir, journal_abbrev)
            args_list.append([url, out_json, tsleep])

    tmp = utils.parallel_call(get_journal_data, args_list, nproc, nretry)

if __name__ == '__main__':

    # # in_url = 'http://www.bioxbio.com/if/html/NAT-COMMUN.html'
    # in_url = sys.argv[1]
    # out_json = 'foo.json'
    # tsleep = 0
    # data, error = get_journal_data(in_url, out_json, tsleep)
    # print(error)

    if len(sys.argv) != 2:
        timestamp = utils.get_timestamp()
    else:
        timestamp = sys.argv[1]

    out_dir = '../data/{}'.format(timestamp)
    subject_json = '../data/{}.subject.json'.format(timestamp)

    data = {}
    if os.path.isfile(subject_json):
        data = utils.load_json(subject_json)
    else:
        data = get_all_journal_links()
        utils.write_json(data, subject_json)

    get_all_journal_data(data, out_dir)
