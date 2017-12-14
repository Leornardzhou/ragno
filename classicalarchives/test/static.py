import requests
import bs4
import json
from string import ascii_lowercase
import re
import random
import time


def get_html(url, wait_time_min=1, wait_time_max=3):
    try:
        # print('> getting URL: {}'.format(url))
        time.sleep(wait_time_min + random.random() *
                   (wait_time_max - wait_time_min))
        r = requests.get(url)
        r.raise_for_status()
        return r.text
    except:
        return '*ERROR*: failed to retrieve {}'.format(url)


def get_composer_urls(fout_name=None):

    composer_urls = []
    domain = 'https://www.classicalarchives.com'
    for x in ascii_lowercase:
        url = '{}/midi/composers/{}.html'.format(domain, x)
        html = get_html(url)
        soup = bs4.BeautifulSoup(html, 'lxml')
        composer_list = soup.find_all('a', href=re.compile(r'/midi/composer/[0-9]*.html'))
        for composer in composer_list:
            composer_urls.append(composer['href'])
    print('> found {} composers'.format(len(composer_urls)))

    if fout_name:
        with open(fout_name, 'w') as f:
            for url in composer_urls:
                print('{}/{}'.format(domain, url), file=f)

    return composer_urls


def parse_composer_name(html):

    soup = bs4.BeautifulSoup(html, 'lxml')
    name = soup.find('h1', class_='composer').text
    return name


def temp_load_html(fname):
    return open(fname).read()


def get_composer_names():

    # get_composer_urls(fout_name='composer_urls.list')

    # load composer urls
    composer_urls = []
    for line in open('composer_urls.list'):
        composer_urls.append(line.rstrip())

    composer_name = {}
    nline = 0
    for url in composer_urls:
        html = get_html(url, wait_time_min=1, wait_time_max=3)
        composer_name[url] = parse_composer_name(html)
        nline += 1
        if nline == 20:
            break

    with open('composer_names.json', 'w') as f:
        print(json.dumps(composer_name, sort_keys=True, indent=4), file=f)


if __name__ == '__main__':

    get_composer_names()
