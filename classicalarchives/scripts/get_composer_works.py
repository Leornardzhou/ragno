import sys
import os
from pyvirtualdisplay import Display

from os.path import abspath, dirname
root_dir = dirname(dirname(abspath(__file__)))
sys.path.append(root_dir)

from classicalarchives import utils
from classicalarchives import composer


def get_composer_works(composers_list_fname, skip_exist=True):

    # start virtual display
    display = Display(visible=0, size=(1024,768))
    display.start()
    driver = utils.start_driver('chrome', verbose=True)

    try:

        for composer_id in open(composers_list_fname):
            composer_id = composer_id.rstrip()
            out_json = '{}/data/composer/{}.json'.format(root_dir, composer_id)
            if skip_exist and os.path.isfile(out_json):
                continue

            nretry = 0
            while nretry < 10:
                try:
                    utils.print_message('extract works of composer {}'
                                        .format(composer_id))
                    c = composer.Composer(driver, composer_id)
                    c.get_all_works()
                    c.format_json(fname_out=out_json)
                    utils.print_message('\n')
                    break

                except:
                    utils.print_message('*ERROR* failed to extract works of '
                                        'composer {} (#retry={})'
                                        .format(composer_id, nretry))
                    utils.wait(3)
                    nretry += 1

    finally:

        utils.close_driver(driver, verbose=True)
        display.stop()


composers_list_fname = sys.argv[1]
get_composer_works(composers_list_fname)
