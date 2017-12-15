import utils
import json
import sys
import os


host = 'https://www.classicalarchives.com'

def check_update(id_csv=None):

    if id_csv:
        id_set = set(id_csv.split(','))
    else:
        id_set = None

    update_composer_id_list = []

    driver = utils.start_driver('phantomjs')
    for composer_id in open('composers.list'):
        composer_id = composer_id.rstrip()
        if id_set and composer_id not in id_set:
            continue
        composer_json = 'composer/{}.json'.format(composer_id)
        composer = utils.load_json(composer_json, verbose=False)

        ntrack = 0
        for work in composer['work_list']:
            for page in work['page_list']:
                for track in page['track_list']:
                    ntrack += 1

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
                nretry += 1

        if ntrack_online != ntrack:
            update_composer_id_list.append(composer_id)
            marker = '<----- mismatch!'
        else:
            marker = ''
        utils.print_message('Composer {}: online {} local {}'
                            .format(composer_id, ntrack_online, ntrack, marker))
    driver.close()

    if len(update_composer_id_list):
        print('samples to update: {}'.format(','.join(update_composer_id_list)))
    else:
        print('all samples are up-to-date.')

if __name__ == '__main__':

    if len(sys.argv) > 1:
        id_csv = sys.argv[1]
    else:
        id_csv = None

    check_update(id_csv=id_csv)
