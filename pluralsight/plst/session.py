import utils

host = 'https://app.pluralsight.com'


def login(driver, credential_json, verbose=True):

    info = utils.load_json(credential_json)
    utils.open_url(driver, host + '/id?redirectTo=%2F', verbose=verbose)
    driver.find_element_by_id('Username').send_keys(info['username'])
    driver.find_element_by_id('Password').send_keys(info['password'])
    driver.find_element_by_id('login').click()


def logout(driver, verbose=True):
    utils.open_url(driver, host + '/id/signout', verbose=verbose)


def is_login(driver, verbose=False):
    try:
        name = driver.find_element_by_xpath(
            '//*[starts-with(@class, "firstName---")]').text
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
