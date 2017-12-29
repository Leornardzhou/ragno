import sys
from selenium import webdriver
import json
import time
import crawler

class Session:


    def __init__(self, driver_type, wait_time=3):

        self.driver_type = driver_type
        if driver_type == 'chrome':
            self.driver = webdriver.Chrome()
        elif driver_type == 'phantomjs':
            self.driver = webdriver.PhantomJS()
        elif driver_type == 'firefox':
            self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(wait_time)
        self.username = None
        self.password = None


    def close(self):
        self.driver.quit()


    def open_url(self, url):
        if self.driver_type == 'phantomjs':
            self.debug_print('getting url: ' + url)
        self.driver.get(url)


    def debug_print(self, msg):
        print('> ' + msg, file=sys.stderr, flush=True)


    def login(self, credential_json):
        info = json.loads(open(credential_json).read())
        self.username = info['username']
        self.password = info['password']

        self.open_url(crawler.login_url)
        crawler.login_username(self.driver).send_keys(self.username)
        crawler.login_password(self.driver).send_keys(self.password)
        crawler.login_button(self.driver).click()


    def logout(self):
        self.open_url(crawler.logout_url)


    def is_login(self):
        try:
            name = crawler.welcome_name(self.driver)
        except:
            name = ''
        if name:
            self.debug_print('Hello {}!'.format(name))
            return True
        else:
            self.debug_print('You not login.')
            return False


    def get_all_composers(self):
        ''' {'info':'', 'url':''} '''
        composer_list = []
        for url in crawler.group_url_list():
            self.open_url(url)
            out = crawler.group_composer_list(self.driver)
            composer_list.extend(out)
            self.debug_print('found {} composers'.format(len(out)))
        return composer_list





def test():

    s = Session('phantomjs', wait_time=0)

    try:
        # s.login('credential.json')
        # s.logout()
        d = s.get_all_composers()
        import utils
        utils.save_json(d, 'foo.json')

    except:
        print('*ERROR*')

    finally:
        time.sleep(5)
    s.close()


if __name__ == '__main__':

    test()
