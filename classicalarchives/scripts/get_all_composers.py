import sys
import os
from string import ascii_lowercase
import datetime

from os.path import abspath, dirname
root_dir = dirname(dirname(abspath(__file__)))
sys.path.append(root_dir)

from classicalarchives import utils
from classicalarchives import composers


def get_all_composers(out_json_fname, out_list_fname):

    driver = utils.start_driver('phantomjs', verbose=True)

    try:
        composer_json = composers.get_all_composers(driver)
        utils.save_json(composer_json, out_json_fname)

        # write composer id list
        composer_id_list = []
        for composer in composer_json:
            composer_id = composer['url'].split('/')[-1].replace('.html', '')
            composer_id_list.append(int(composer_id))

        fout = open(out_list_fname, 'w')
        utils.print_message('wrinting composer ID list ' + out_list_fname)
        for composer_id in sorted(composer_id_list):
            print(composer_id, file=fout)
        fout.close()

    finally:
        utils.close_driver(driver, verbose=True)




if __name__ == '__main__':

    timestamp = datetime.datetime.today().strftime("%Y%m%d%H%M")
    out_json_fname = '{}/data/composers_{}.json'.format(root_dir, timestamp)
    out_list_fname = '{}/data/composers_{}.list'.format(root_dir, timestamp)

    get_all_composers(out_json_fname, out_list_fname)
