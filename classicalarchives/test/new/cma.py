from selenium import webdriver
import sys
import time


class CMASession:


    domain_url = 'https://www.classicalarchives.com'
    login_url = domain_url + '/secure/login.html'
    logout_url = domain_url + '/secure/logout.html'
    account_url = domain_url + '/secure/youraccount.html'
    download_url = domain_url + '/secure/downloads.html'


    def __init__(self, wait_time=5, verbose=False):
        self.__username = None
        self.__password = None
        self.__login_status = False
        self.__verbose = verbose
        self.print('starting browser ...')
        self.__browser = webdriver.PhantomJS()  # default url: "about:blank"
        self.__browser.implicitly_wait(wait_time)


    def print(self, msg):
        if self.__verbose:
            print('>> ' + msg, file=sys.stderr, flush=True)


    def close(self):
        self.print('closing browser')
        self.__browser.close()


    def snapshot(self, img_name):
        self.__browser.save_screenshot(img_name)
        self.print('saved snapshot to {}'.format(img_name))


    def login(self, username, password):
        self.__username = username
        self.__password = password
        self.print('login {}'.format(self.__username))
        self.__browser.get(self.login_url)
        self.__find_login_username().send_keys(username)
        self.__find_login_password().send_keys(password)
        self.__find_login_bottun().click()


    def logout(self):
        self.print('logout {}'.format(self.__username))
        self.__browser.get(self.logout_url)
        self.__username = None
        self.__password = None


    def is_login(self):
        if self.__browser.current_url == 'about:blank':
            return False
        name = self.__find_member_name()
        if name:
            self.print('You are login as {}'.format(name))
            return True
        else:
            self.print('You are not login')
            return False


    def wait(self, sleep_time):
        self.print('wait for {} seconds'.format(sleep_time))
        time.sleep(sleep_time)


    # --------------------------------------------------

    def __find_login_username(self):
        elem = self.__browser.find_element_by_id('email')
        return elem

    def __find_login_password(self):
        elem = self.__browser.find_element_by_id('password')
        return elem

    def __find_login_bottun(self):
        xpath = ('//*[@id="signinbtn"]//button')
        elem = self.__browser.find_element_by_xpath(xpath)
        return elem

    def __find_member_name(self):
        # elem_list = self.__browser.find_elements_by_id('cma-header-member-welcome')
        elem_list = self.__browser.find_elements_by_id('welcome-name')
        name = ''
        for elem in elem_list:
            name += elem.text
        return name


def test():

    sess = CMASession(verbose=True)
    sess.is_login()
    sess.login('joeyfuerimmer@gmail.com', '0.567359Zy')
    sess.is_login()
    sess.wait(10)
    sess.logout()
    sess.is_login()
    sess.snapshot('foo.png')
    sess.close()


if __name__ == '__main__':

    test()
