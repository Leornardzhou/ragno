'''This module works with /midi/composers/x.html '''

from string import ascii_lowercase
from . import utils


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
        utils.print_message('Found {} composers'.format(len(elem_list)))

    result = []
    for elem in elem_list:
        result.append({'composer': elem.text,
                       'url': elem.get_attribute('href')})

    return result


def get_all_composers(driver, verbose=True):
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

    return result
