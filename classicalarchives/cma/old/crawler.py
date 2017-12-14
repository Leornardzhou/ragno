"""In case the crawler stop working, fix here
"""

from string import ascii_lowercase

domain = 'https://www.classicalarchives.com'
login_url = domain + '/secure/login.html'
logout_url = domain + '/secure/logout.html'


def login_username(driver):
    return driver.find_element_by_id('email')


def login_password(driver):
    return driver.find_element_by_id('password')


def login_button(driver):
    return driver.find_element_by_xpath('//button[@type="submit"]')


def welcome_name(driver):
    return driver.find_element_by_id('welcome-name').text


def group_url_list():
    return [domain + '/midi/composers/{}.html'.format(x)
            for x in ascii_lowercase]


def group_composer_list(driver):
    out = []
    for elem in driver.find_elements_by_xpath('//a[starts-with(@href, '
                                              '"/midi/composer/")]'):
        out.append({'composer': elem.text,
                    'url': elem.get_attribute('href')})
    return out
