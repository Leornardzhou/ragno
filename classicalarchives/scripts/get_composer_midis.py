import time
import json
from pyvirtualdisplay import Display

import sys
import os

from os.path import abspath, dirname
root_dir = dirname(dirname(abspath(__file__)))
sys.path.append(root_dir)

from classicalarchives import utils
from classicalarchives import composer
from classicalarchives import download
from classicalarchives import session


def get_composer_midis(midi_list_fname):

    utils.print_message('---------- Start Time: {} ----------'.format(time.ctime()))

    # start virtual display
    display = Display(visible=0, size=(1024,768))
    display.start()

    credential = '{}/data/cma.credential.json'.format(root_dir)
    driver = utils.start_driver('chrome', verbose=True)

    try:

        session.login(driver, credential)
        utils.wait(3)
        utils.print_message(' ')

        ntrack = 0
        ntrack_max = 103   # 100 midis/day
        for line in open(midi_list_fname):

            composer_id, work_id, page_id, track_id = map(
                int, line.rstrip().split(','))

            out_dir = '{}/data/midi/{}'.format(root_dir, composer_id)
            os.makedirs(out_dir, exist_ok=True)
            fname_prefix = 'composer_{}.work_{}.page_{}.track_{}'.format(
                composer_id, work_id, page_id, track_id)

            # check if output midi already exists
            file_exist = False
            for local_fname in os.listdir(out_dir):
                if local_fname.startswith(fname_prefix + '.'):
                    file_exist = True
            if file_exist:
                continue

            # create a download job
            job = download.Download(
                driver, composer_id, work_id, page_id, track_id)
            job.order()
            utils.wait(5)

            # check if a download is successfully created
            success = False
            fname = job.pickup(out_dir)
            if fname:
                success = job.cleanup()
            if not success:
                break

            utils.print_message('successfully downloaded {} ({}/100)'
                                .format(job.track.title, ntrack+1))
            utils.print_message('output file: {}'.format(fname))
            utils.print_message(' ')
            utils.wait(3)

            ntrack += 1

            # if daily limit is reached
            if ntrack == ntrack_max:
                break

    finally:

        utils.print_message(' ')
        session.logout(driver)
        utils.wait(3)
        utils.close_driver(driver, verbose=True)
        display.stop()


    utils.print_message('---------- Finish Time: {} ----------'.format(time.ctime()))



if __name__ == '__main__':

    midi_list_fname = sys.argv[1]
    get_composer_midis(midi_list_fname)
