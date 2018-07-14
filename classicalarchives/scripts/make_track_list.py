import json
import sys
import os

from os.path import abspath, dirname
root_dir = dirname(dirname(abspath(__file__)))
sys.path.append(root_dir)

from classicalarchives import utils


def make_track_list(composers_list_fname, out_list_fname):

    data_dir = os.path.dirname(composers_list_fname)

    fout = open(out_list_fname, 'w')
    for composer_id in open(composers_list_fname):

        composer_id = composer_id.rstrip()
        composer_json = '{}/composer/{}.json'.format(data_dir, composer_id)
        composer = utils.load_json(composer_json, verbose=False)
        composer_id = composer['composer_id'].replace('composer_','')
        for work in composer['work_list']:
            work_id = work['work_id'].replace('work_','')
            for page in work['page_list']:
                page_id = page['page_id'].replace('page_','')
                for track in page['track_list']:
                    track_id = track['track_id'].replace('track_','')
                    print('{},{},{},{}'.format(composer_id, work_id,
                                               page_id, track_id), file=fout)
    fout.close()


composers_list_fname = sys.argv[1]
out_list_fname = sys.argv[2]
make_track_list(composers_list_fname, out_list_fname)
