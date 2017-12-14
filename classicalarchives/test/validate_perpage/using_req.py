import sys
from bs4 import BeautifulSoup as BS
import re
import json

def foo(fname):

    html = open(fname).read()
    soup = BS(html, 'lxml')

    res = {}

    # get composer id from url
    res['id'] = re.findall(r'([0-9]*).html', fname)[0]

    # get composer name, birth/death, country
    res['info'] = soup.find('h1', class_='composer').text

    midi_tag = soup.find('div', id='wMidi')

    # get #midi
    nmidi = midi_tag.find('li', class_='counts').text
    res['nmidi'] = int(nmidi.split()[1].replace(',',''))

    res['work'] = {}

    # get meta data of all midis (default class='toggle')
    for x in midi_tag.find_all('li', class_='toggle'):
        group_id = x['id']
        work = x.find('a', id=re.compile(r'^work_'))
        work_id = work['id']
        work_name = work.text.strip()
        nmidi = int(x.find('div', class_='infolabel').text.strip().split()[0])
        res['work'][work_id] = {'group_id':group_id, 'name':work_name, 'nmidi': nmidi}

    print(json.dumps(res, sort_keys=True, indent=4))



fname = sys.argv[1]
foo(fname)
