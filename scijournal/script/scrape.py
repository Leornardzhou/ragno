import os
import json
import sys
from kit import utils
import requests
import time
from lxml import etree
from urllib.parse import urljoin
import re
from string import ascii_uppercase

host = 'https://www.scijournal.org'

def get_journal_data(in_url, out_json, tsleep):
    '''Get journal data (name, issn, impact factors) from input URL
    https://www.scijournal.org/impact-factor-of-ACM-SIGPLAN-NOTICES.shtml
    and get URL of next/previous journals
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

        data = {}
        data['url'] = in_url
        x = root.xpath('//h1')[0].text
        data['title'] = x.replace('Impact Factor','').strip()

        x = re.findall(r'Journal Abbreviation: (.*?)<br>', r.text)
        data['title_abbrev'] = x[0] if x else None

        x = re.findall('Journal ISSN: (.*?)$', r.text, re.MULTILINE)
        data['issn'] = x[0] if x else None

        data['impact'] = {}
        years = ['2016/2017']
        for i in range(2008, 2016):
            years.append(str(i))
        for year in years:
            x = re.findall(r'{} Impact Factor : (.*?)<br>'.format(year), r.text)
            data['impact'][year] = x[0] if x else '-NA-'

        utils.write_json(data, out_json)

    except Exception as e:
        error = '*ERROR* ' + str(e)
        data = {}

    return data, error


def get_journal_links(in_url, tsleep):
    '''Get all journal links under input URL
    https://www.scijournal.org/list-of-impact-factor-journal_A.shtml
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
        for a in text.xpath('//center/h2/a'):
            title = a.text
            url = a.get('href')
            if not url.startswith('impact-factor-of-'):
                continue
            url = urljoin(host, url)
            data[url] = title

    except Exception as e:
        error = '*ERROR* ' + str(e)
        data = {}

    return data, error


def get_all_journal_links(nproc=3, nretry=10, tsleep=1):
    '''Get urls of all journals'''

    subject_names = [
        'agriculture-and-forestry', 'astronomy', 'biology',
        'chemistry', 'engineering', 'environmental-science', 'geoscience',
        'medicine', 'math', 'management-science', 'physics', 'social-science',
    ]

    subject_list = [
        '{}/{}-journal-impact-factor-list.shtml'.format(host, x)
        for x in subject_names
    ]

    number_list = [
        '{}/list-of-impact-factor-journal_{}.shtml'.format(host, x)
        for x in range(1,91)
    ]

    alphabet_list = [
        '{}/list-of-impact-factor-journal_{}.shtml'.format(host, x)
        for x in ascii_uppercase
    ]

    url_set = set(subject_list)
    url_set.update(set(number_list))
    url_set.update(set(alphabet_list))

    args_list = []
    for url in sorted(url_set):
        args_list.append([url, tsleep])

    tmp = utils.parallel_call(get_journal_links, args_list, nproc, nretry)

    data = {}
    for x in tmp:
        for k,v in x.items():
            data[k] = v

    utils.qprint('get urls of {} journals'.format(len(data)))

    return data


def get_all_journal_data(all_journal_dict, out_dir,
                         nproc=3, nretry=10, tsleep=1):
    '''Get data of all journals'''

    os.makedirs(out_dir, exist_ok=True)

    args_list = []
    for url in sorted(all_journal_dict):
        journal_abbrev = re.findall(r'/impact-factor-of-(.*?).shtml',
                                    url)[0].lower()
        out_json = '{}/{}.json'.format(out_dir, journal_abbrev)
        args_list.append([url, out_json, tsleep])

    args_list = [x for x in sorted(args_list, key=lambda x: x[0])]
    utils.parallel_call(get_journal_data, args_list, nproc, nretry)



def test():

    # data, error = get_journal_links(
    #     # 'https://www.scijournal.org/list-of-impact-factor-journal_Z.shtml',
    #     'https://www.scijournal.org/agriculture-and-forestry-journal-impact-factor-list.shtml',
    #     0)

    # url = 'https://www.scijournal.org/impact-factor-of-NAT-REV-CANCER.shtml'
    # url = 'https://www.scijournal.org/impact-factor-of-HEALTH-INFORM-J.shtml'
    # data, error = get_journal_data(
    #     url,
    #     # 'https://www.scijournal.org/impact-factor-of-NATURE.shtml',
    #     'foo.json', 0)
    # print(json.dumps(data, sort_keys=True, indent=2))
    # print(len(data))
    # print(error)

    data = get_all_journal_links(nproc=3, nretry=10, tsleep=1)
    utils.write_json(data, 'foo.json')




if __name__ == '__main__':

    # test()

    if len(sys.argv) != 2:
        timestamp = utils.get_timestamp()
    else:
        timestamp = sys.argv[1]

    out_dir = '../data/{}'.format(timestamp)
    url_json = '../data/{}.url.json'.format(timestamp)

    data = {}
    if os.path.isfile(url_json):
        data = utils.load_json(url_json)
    else:
        data = get_all_journal_links()
        utils.write_json(data, url_json)

    get_all_journal_data(data, out_dir)
