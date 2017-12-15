import json
import driver
import utils


def login(driver):
    driver.open(url)


class Session:


    cma_domain = 'https://www.classicalarchives.com'


    def __init__(self, driver):

        self.username = None
        self.password = None


    def login(self, credential_json):
        info = json.loads(open(credential_json).read())
        self.username = info['username']
        self.password = info['password']

        self.driver.open_url(self.cma_domain + '/secure/login.html')
        self.driver.driver.find_element_by_id('email').send_keys(self.username)
        self.driver.driver.find_element_by_id('password').send_keys(self.password)
        self.driver.find_element_by_xpath('//button[@type="submit"]').click()


    def logout(self):
        self.username = None
        self.password = None
        self.open_url(self.cma_domain + '/secure/logout.html')


    def is_login(self):
        try:
            name = self.driver.find_element_by_id('welcome-name').text
        except:
            name = ''
        if name:
            utils_debug_print('Hello {}!'.format(name))
            return True
        else:
            utils_debug_print('You not login.')
            return False
