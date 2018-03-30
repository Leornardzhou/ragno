'''This program scrapes all data at URL
http://www.chinahpo.org/wiki/index.php/Omim_disease_list

Watch out as the web page contains duplicated diseases, the unqiue number of
dieases is not 5271 as claimed.
'''

import os
from os.path import dirname, abspath
import requests
from kit import utils
from lxml import etree


def get_list(out_json):

    out_dir = abspath(dirname(out_json))
    os.makedirs(out_dir, exist_ok=True)

    url = ('http://www.chinahpo.org/wiki/index.php/Omim_disease_list')

    data = dict()
    error = None
    try:
        utils.qprint('get ' + url)
        r = requests.get(url)
        if not r.ok:
            raise
        text = r.text

        # utils.write_html(r.text, 'foo.html')
        # text = utils.load_html('foo.html')

        text = etree.HTML(text)

        for tr in text.xpath('//tr'):
            td_list = tr.xpath('./td')
            if len(td_list) < 3:
                continue
            omim_id = td_list[0].text.strip()
            name_en = td_list[1].text.strip()
            name_cn = td_list[2].text.strip()

            # if you want to see the duplicates
            # if omim_id in data:
            #     utils.qprint('duplicate omim id: ' + omim_id)

            data[omim_id] = {
                'name_en': name_en,
                'name_cn': name_cn,
            }

        utils.qprint('found {} unique diseases'.format(len(data)))
        utils.write_json(data, out_json)

    except Exception as e:
        error = '*ERROR* ' + str(e)
        data = dict()
        print(error)



    return data, error



if __name__ == '__main__':

    out_json = '../data/short_list/omim_diseases.json'
    data, error = get_list(out_json)
