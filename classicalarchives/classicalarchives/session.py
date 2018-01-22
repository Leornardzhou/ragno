from . import utils

host = 'https://www.classicalarchives.com'

def login(driver, credential_json, verbose=True):

    info = utils.load_json(credential_json)
    utils.open_url(driver, host + '/secure/login.html', verbose=verbose)
    driver.find_element_by_id('email').send_keys(info['username'])
    driver.find_element_by_id('password').send_keys(info['password'])
    driver.find_element_by_xpath('//button[@type="submit"]').click()


def logout(driver, verbose=True):
    utils.open_url(driver, host + '/secure/logout.html', verbose=verbose)


def is_login(driver, verbose=False):
    try:
        name = driver.find_element_by_id('welcome-name').text
    except:
        name = None
    if name:
        if verbose:
            utils.print_message('Hello {}!'.format(name))
        return True
    else:
        if verbose:
            utils.print_message('You are not login.')
        return False
