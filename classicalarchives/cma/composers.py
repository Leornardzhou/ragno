'''This module works with /midi/composers/x.html '''

import utils
from string import ascii_lowercase


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


if __name__ == '__main__':

    import utils
    import sys
    out_name = sys.argv[1]

    driver = utils.start_driver('phantomjs')
    get_all_composers(driver, out_name)
    driver.close()
