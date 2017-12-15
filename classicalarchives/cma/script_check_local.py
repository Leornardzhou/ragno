import utils
import json
import sys
import os


def check():

    for composer_id in open('composers.list'):
        composer_id = composer_id.rstrip()
        composer_json = 'composer/{}.json'.format(composer_id)
        composer = utils.load_json(composer_json, verbose=False)

        ntrack = 0
        for work in composer['work_list']:
            for page in work['page_list']:
                for track in page['track_list']:
                    ntrack += 1

        if composer['ntrack'] != ntrack:
            print(composer_json, composer['ntrack'], ntrack)

check()
