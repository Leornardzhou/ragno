from os.path import abspath, dirname
package_path = dirname(dirname(dirname(abspath(__file__))))

import sys
sys.path.append(package_path)


from classicalarchives import utils
from classicalarchives import session
from classicalarchives import composer
from classicalarchives import download


credential = '{}/data/cma.credential.json'.format(package_path)


def test_login():

    driver = utils.start_driver('phantomjs', verbose=True)

    try:
        session.login(driver, credential)
        utils.wait(5)
        session.is_login(driver, verbose=True)
        utils.wait(5)
        session.logout(driver)

    finally:
        utils.close_driver(driver, verbose=True)


def test_get_composer_data():

    composer_id = '2062'
    out_json = '2062.json'

    driver = utils.start_driver('phantomjs', verbose=True)

    try:
        c = composer.Composer(driver, composer_id)
        c.get_all_works()
        c.format_json(fname_out=out_json)

    finally:
        utils.close_driver(driver, verbose=True)


def test_download_midi():

    argv = '2013,31394,1,1'

    driver = utils.start_driver('phantomjs', verbose=True)

    try:
        session.login(driver, credential)
        composer_id, work_id, page_id, track_id = map(int, argv.split(','))

        out_dir = 'midi/{}'.format(composer_id)
        job = download.Download(driver, composer_id, work_id, page_id, track_id)
        job.order()
        utils.wait(3)
        success = False
        fname = job.pickup(out_dir)
        if fname:
            success = job.cleanup()
        if success:
            utils.print_message('successfully downloaded {}'.format(job.track.title))
            utils.print_message('output file: {}'.format(fname))
        utils.wait(3)
        session.logout(driver)

    finally:
        utils.close_driver(driver, verbose=True)


# test_login()
# test_get_composer_data()
test_download_midi()
