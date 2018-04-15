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
    and get URL of next/previous journals
    '''

    data = {'done': [], 'todo': []}
    error = None

    try:
        utils.qprint('get ' + in_url)
        r = requests.get(in_url)
        if not r.ok:
            raise
        time.sleep(tsleep)
        root = etree.HTML(r.text)

        if not os.path.isfile(out_json):

            jdata = {}
            jdata['url'] = in_url
            jdata['title'] = root.xpath('//div/h1')[0].text
            x = re.findall(r'<p>Journal Abbreviation: (.*?)<br>', r.text)
            jdata['title_abbrev'] = x[0] if x else x
            x = re.findall(r'Journal ISSN: (.*?)</p>', r.text)
            jdata['issn'] = x[0] if x else x

            jdata['impact'] = {}
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
                jdata['impact'][year] = {
                    'ifact': ifact, 'npub': npub,
                }

            utils.write_json(jdata, out_json)

        data['done'].append(in_url)

        # get prev and next url
        a = root.xpath('//div[@class="col-md-6 col-sm-12 text-left"]/a')
        data['todo'].append(
            'http://www.bioxbio.com/if/html/' + a[0].get('href'))
        a = root.xpath('//div[@class="col-md-6 col-sm-12 text-right"]/a')
        data['todo'].append(
            'http://www.bioxbio.com/if/html/' + a[0].get('href'))

    except Exception as e:
        error = '*ERROR* ' + str(e)
        data = []

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
            journal_abbrev = re.findall(r'/if/html/(.*?).html',
                                        url)[0].lower()
            out_json = '{}/{}.json'.format(out_dir, journal_abbrev)
            args_list.append([url, out_json, tsleep])

    args_list = [x for x in sorted(args_list, key=lambda x: x[0])]
        #     if len(args_list) > 10:
        #         break
        # if len(args_list) > 10:
        #     break

    done_set = set()
    cycle = 0
    while True:
        tmp = utils.parallel_call(get_journal_data, args_list, nproc, nretry)
        cycle += 1

        todo_set = set()
        for x in tmp:
            for url in x['done']:
                done_set.add(url)
            for url in x['todo']:
                todo_set.add(url)

        todo_set = todo_set - done_set
        if len(todo_set) == 0:
            break

        args_list = []
        for url in sorted(todo_set):
            journal_abbrev = re.findall(r'/if/html/(.*?).html',
                                        url)[0].lower()
            out_json = '{}/{}.json'.format(out_dir, journal_abbrev)
            args_list.append([url, out_json, tsleep])

        utils.qprint('after cycle {}, get {} new journals'
                     .format(cycle, len(args_list)))

# def catch_missing(timestamp, tsleep=1):

#     subject_json = '../data/{}.subject.json'.format(timestamp)
#     data = utils.load_json(subject_json)
#     url_set = set()
#     for subj in data:
#         for url in data[subj]:
#             url_set.add(url)

#     min_url = sorted(url_set)[0]
#     utils.qprint('starting from ' + min_url)

#     novel_url_set = set()
#     url = min_url
#     count = 0
#     count_max = 100000
#     while True:
#         journal_abbrev = re.findall(r'/if/html/(.*?).html', url)[0].lower()
#         out_json = '../data/{}/'
#         get_journal_data(next_url, out_json, tsleep)

#         r = requests.get(url)
#         time.sleep(tsleep)
#         if not r.ok:
#             raise '*ERROR*: can not retrieve ' + url
#         root = etree.HTML(r.text)
#         a = root.xpath('//div[@class="col-md-6 col-sm-12 text-right"]/a')
#         next_url = 'http://www.bioxbio.com/if/html/' + a[0].get('href')
#         if next_url not in url_set:
#             novel_url_set.add(next_url)



#         url = next_url
#         if url == min_url:
#             break
#         count += 1
#         if count == count_max:
#             break


# def get_all_journal_data(all_journal_dict, out_dir,
#                          nproc=3, nretry=10, tsleep=1):
#     '''Get data of all journals'''

#     os.makedirs(out_dir, exist_ok=True)

#     args_list = []
#     for subject in sorted(all_journal_dict):
#         for url in sorted(all_journal_dict[subject]):
#             journal_abbrev = re.findall(r'/if/html/(.*?).html', url)[0].lower()
#             out_json = '{}/{}.json'.format(out_dir, journal_abbrev)
#             args_list.append([url, out_json, tsleep])

#     tmp = utils.parallel_call(get_journal_data, args_list, nproc, nretry)

def test():

    data, error = get_journal_data(
        'http://www.bioxbio.com/if/html/Z-PADAGOGIK.html',
        'foo.json', 0)
    print(data)
    print(error)



if __name__ == '__main__':

    # timestamp = '201804140057'
    # catch_missing(timestamp)
    # test()


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
