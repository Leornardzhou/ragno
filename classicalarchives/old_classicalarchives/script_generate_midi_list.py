import utils
import json
import sys
import os


def check():

    for composer_id in open('composers.list'):
        composer_id = composer_id.rstrip()
        composer_json = 'composer/{}.json'.format(composer_id)
        composer = utils.load_json(composer_json, verbose=False)
        composer_id = composer['composer_id'].replace('composer_','')
        for work in composer['work_list']:
            work_id = work['work_id'].replace('work_','')
            for page in work['page_list']:
                page_id = page['page_id'].replace('page_','')
                for track in page['track_list']:
                    track_id = track['track_id'].replace('track_','')
                    print('{},{},{},{}'.format(composer_id, work_id,
                                               page_id, track_id))

check()
