'''This program extracts data of a game at http://steamspy.com/app/XXXXXX
'''

import sys
from selenium import webdriver
import json
import re
import os

def get_game_data(driver, game_url, out_fname):

    print('open ' + game_url, file=sys.stderr)
    driver.get(game_url)

    # get game data chunk
    elem_game_name = driver.find_element_by_tag_name('h3')
    game_name = elem_game_name.text

    elem_game_data = elem_game_name.find_element_by_xpath('../../p')
    game_data_text = elem_game_data.text
    # game_data_text = elem_game_data.get_attribute('innerHTML')

    print('parse data of game: ' + game_name, file=sys.stderr)
    game_data = dict()
    game_data['Raw'] = game_data_text
    game_data['Name'] = game_name

    for line in game_data_text.split('\n'):
        if line.startswith('Store'):
            continue

        if line.startswith('Developer:'):
            x = line.split('Publisher:')
            dev = x[0].split(': ')[1]
            pub = x[1].lstrip()
            game_data['Developer'] = dev
            game_data['Publisher'] = pub

        elif line.startswith('Genre:'):
            game_data['Genre'] = line.split(': ')[1].split(', ')

        elif line.startswith('Languages:'):
            game_data['Languages'] = line.split(': ')[1].split(', ')

        elif line.startswith('Tags:'):
            game_data['Tags'] = []
            tag_list = line.split(': ')[1].split(', ')
            for x in tag_list:
                tag, rate = re.findall(r'(.*?) \((\d+)\)$', x)[0]
                game_data['Tags'].append([tag, int(rate)])

        elif line.startswith('Category:'):
            game_data['Category'] = line.split(': ')[1].split(', ')

        elif line.startswith('Release date:'):
            game_data['Release date'] = line.split(':')[1].lstrip()

        elif line.startswith('Price:'):
            game_data['Price'] = line.split(': ')[1]

        elif line.startswith('Score rank:'):
            if 'Metascore' in line:
                scores = re.findall(r'Score rank: (.*?)% Userscore: (.*?)% '
                                    'Old userscore: (.*?)% Metascore: (.*?)%$',
                                    line)[0]
                game_data['Scores'] = {
                    'rank': int(scores[0]), 'user': int(scores[1]),
                    'old': int(scores[2]), 'meta': int(scores[3]),
                }
            else:
                scores = re.findall(r'Score rank: (.*?)% Userscore: (.*?)% '
                                    'Old userscore: (.*?)%$', line)[0]
                game_data['Scores'] = {
                    'rank': int(scores[0]), 'user': int(scores[1]),
                    'old': int(scores[2]), 'meta': -1,
                }

        elif line.startswith('Owners:'):
            game_data['Owners'] = line.split(': ')[1]

        elif line.startswith('Players in the last 2 weeks:'):
            game_data['Players in the last 2 weeks'] = line.split(': ')[1]

        elif line.startswith('Players total:'):
            game_data['Players total'] = line.split(': ')[1]

        elif line.startswith('Followers:'):
            game_data['Followers'] = line.split(': ')[1]

        elif line.startswith('Peak concurrent players yesterday:'):
            game_data['Peak concurrent players yesterday'] = line.split(': ')[1]

        elif line.startswith('YouTube stats:'):
            game_data['YouTube stats'] = line.split(': ')[1]

        elif line.startswith('Playtime in the last 2 weeks:'):
            game_data['Playtime in the last 2 weeks'] = line.split(': ')[1]

        elif line.startswith('Playtime total:'):
            game_data['Playtime total'] = line.split(': ')[1]

    print('writing ' + out_fname, file=sys.stderr)
    fout = open(out_fname, 'w')
    print(json.dumps(game_data, sort_keys=True), file=fout)
    fout.close()


def main(game_url_list, cookies_fname):

    cookies = json.loads(open(cookies_fname).read())

    driver = webdriver.Chrome()
    try:
        # load cookies
        driver.get('http://steamspy.com')
        for c in cookies:
            driver.add_cookie(c)

        for game_url in open(game_url_list):
            game_url = game_url.rstrip()
            game_index = game_url.split('/')[-1]
            out_fname = 'data/{}.json'.format(game_index)
            if os.path.isfile(out_fname):
                continue
            get_game_data(driver, game_url, out_fname)

    except:

        print('*ERROR* something wrong', file=sys.stderr)
        raise

    finally:
        driver.close()


if __name__ == '__main__':

    # game_url = 'http://steamspy.com/app/477160'
    game_url_list = 'url.list'
    cookies_fname = 'cookies/cookies.json'

    main(game_url_list, cookies_fname)
