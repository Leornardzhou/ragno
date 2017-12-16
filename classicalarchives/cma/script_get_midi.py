import utils
import composer
import os
import session
import sys
import download


driver = utils.start_driver('chrome')
session.login(driver, '/Users/zyhuang/cma.credential.json')
utils.wait(3)

ntrack = 0
ntrack_max = 90
for line in open('midi.list'):

    composer_id, work_id, page_id, track_id = map(
        int, line.rstrip().split(','))

    out_dir = 'midi/{}'.format(composer_id)
    os.makedirs(out_dir, exist_ok=True)
    fname_prefix = 'composer_{}.work_{}.page_{}.track_{}'.format(
        composer_id, work_id, page_id, track_id)

    file_exist = False
    for local_fname in os.listdir(out_dir):
        if local_fname.startswith(fname_prefix + '.'):
            file_exist = True
    if file_exist:
        continue

    job = download.Download(
        driver, composer_id, work_id, page_id, track_id)
    job.order()
    utils.wait(5)

    success = False
    fname = job.pickup(out_dir)
    if fname:
        success = job.cleanup()
    if success:
        utils.print_message(
            'successfully downloaded {}'.format(job.track.title))
        utils.print_message('output file: {}'.format(fname))
        print()
        utils.wait(3)
    else:
        break

    ntrack += 1
    if ntrack == ntrack_max:
        break

print()
session.logout(driver)
utils.wait(3)
utils.close_driver(driver)
