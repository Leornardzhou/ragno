import utils
import composers
import time
import session
import sys

def test_login():

    driver = utils.start_driver('phantomjs', verbose=True)

    session.login(driver, 'input/credential.json', verbose=True)
    utils.wait(5, verbose=True)

    session.is_login(driver, verbose=True)
    utils.wait(5, verbose=True)

    session.logout(driver, verbose=True)
    utils.wait(5, verbose=True)

    session.is_login(driver, verbose=True)
    utils.wait(5, verbose=True)

    utils.close_driver(driver, verbose=True)

def test_all_composers():

    driver = utils.start_driver('phantomjs', verbose=True)
    composers.get_all_composers(driver, fname_out='foo.json', verbose=True)
    utils.close_driver(driver, verbose=True)


if __name__ == '__main__':

    # test_login()
    # test_all_composers()
