import json
import sys
import os

from os.path import abspath, dirname
root_dir = dirname(dirname(abspath(__file__)))
sys.path.append(root_dir)

from classicalarchives import utils


def check_composer_ntrack(composers_list_fname, online_mode):

    host = 'https://www.classicalarchives.com'
    composer_dir = '{}/data/composer'.format(root_dir)

    mismatch_list = []
    if online_mode:
        driver = utils.start_driver('phantomjs', verbose=True)

    try:
        for composer_id in open(composers_list_fname):
            composer_id = composer_id.rstrip()
            composer_json = '{}/{}.json'.format(composer_dir, composer_id)
            composer = utils.load_json(composer_json, verbose=False)

            ntrack = 0
            for work in composer['work_list']:
                for page in work['page_list']:
                    for track in page['track_list']:
                        ntrack += 1

            if not online_mode:
                if composer['ntrack'] != ntrack:
                    mismatch_list.append(composer_id)
                continue

            # online mode
            ntrack_online = 0
            nretry = 0
            while nretry < 10:
                try:
                    utils.open_url(driver, host + '/midi/composer/{}.html'
                                   .format(composer_id), reopen=True)
                    ntrack_online = int(driver.find_element_by_xpath(
                        '//div[@id="wMidi"]//li[@class="counts"]').text.split()[1].replace(',',''))
                    break
                except:
                    utils.print_message('*ERROR* failed to extract #track for '
                                        'composer {} (#retry={})'
                                        .format(composer_id, nretry))
                    utils.wait(3)
                    nretry += 1

            print('composer={}, #track online={} local={}'
                  .format(composer_id, ntrack_online, ntrack))

            if ntrack_online != ntrack:
                mismatch_list.append(composer_id)


    finally:
        if online_mode:
            utils.close_driver(driver, verbose=True)

    print('Found {} composers with inconsistent #tracks ({} mode)\n'
          .format(len(mismatch_list), 'online' if online_mode else 'local'))

    for composer_id in mismatch_list:
        print(composer_id)



if __name__ == '__main__':

    composers_list_fname = sys.argv[1]
    mode = sys.argv[2]     # local / online
    if mode in ['local', 'online']:
        online_mode = bool(mode == 'online')
    else:
        print('*ERROR*: mode must be local/online')
        sys.exit(0)

    check_composer_ntrack(composers_list_fname, online_mode)
