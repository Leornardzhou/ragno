'''This module works with /midi/composers/x.html '''

import os
import sys
from string import ascii_lowercase
import datetime

script_dir = os.path.abspath(os.path.dirname(__file__))
home_dir = os.path.dirname(script_dir)
sys.path.append(home_dir)
import utils


host = 'https://www.classicalarchives.com'

def get_all_composers_with_initial(driver, initial, verbose=True):
    '''Get all composers starting with initial letter.

    Args:
        driver:  WebDriver object
        initial:  initial letter (a..z)
        verbose:  whether to print progress messages

    Return:
        a list of dictionary {'composer':xxx, 'url':yyy}
    '''

    url = host + '/midi/composers/{}.html'.format(initial)
    utils.open_url(driver, url, verbose=verbose)

    elem_list = driver.find_elements_by_xpath('//a[starts-with(@href, '
                                              '"/midi/composer/")]')
    if verbose:
        utils.print_message('Found {} in URL {}'.format(len(elem_list), url))

    result = []
    for elem in elem_list:
        result.append({'composer': elem.text,
                       'url': elem.get_attribute('href')})

    return result


def get_all_composers(driver, fname_out=None, verbose=True):
    '''Get all composers with initials range from a to z.

    Args:
        driver:  WebDriver object
        verbose:  whether to print progress messages

    Return:
        a list of dictionary {'composer':xxx, 'url':yyy}
    '''

    result = []

    for initial in ascii_lowercase:
        result.extend(get_all_composers_with_initial(driver, initial,
                                                     verbose=verbose))
    if fname_out:
        utils.save_json(result, fname_out)

    return result


def get_composer_ids(composer_json, fname_out):

    composer_id_list = []
    for composer in composer_json:
        composer_id = composer['url'].split('/')[-1].replace('.html', '')
        composer_id_list.append(int(composer_id))

    fout = open(fname_out, 'w')
    utils.print_message('wrinting composer ID list ' + fname_out)
    for composer_id in sorted(composer_id_list):
        print(composer_id, file=fout)
    fout.close()


if __name__ == '__main__':

    timestamp = datetime.datetime.today().strftime("%Y%m%d%H%M")
    out_json_name = '{}/data/composers_{}.json'.format(home_dir, timestamp)
    out_list_name = '{}/data/composers_{}.list'.format(home_dir, timestamp)

    driver = utils.start_driver('phantomjs')
    try:
        composer_json = get_all_composers(driver, out_json_name)
        get_composer_ids(composer_json, out_list_name)
    finally:
        driver.close()
