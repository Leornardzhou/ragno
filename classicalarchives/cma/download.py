import utils
import composer
import os
import pathlib


host = 'https://www.classicalarchives.com'

class Download:

    def __init__(self, driver, composer_id, work_id, page_id, track_id):
        # _id are all integers

        self.driver = driver
        self.composer_id = composer_id
        self.work_id = work_id
        self.page_id = page_id
        self.track_id = track_id

        self.composer = composer.Composer(driver, composer_id)
        self.work = self.composer.get_work_by_id(work_id)
        self.page = self.work.get_page_by_id(page_id)
        self.track = self.page.get_track_by_id(track_id)


    def order(self):
        utils.print_message('order track {}'.format(self.track.title))
        self.track.download()
        utils.wait(5)


    def pickup(self, download_dir):

        os.makedirs(download_dir, exist_ok=True)
        fname_prefix = '{}/composer_{}.work_{}.page_{}.track_{}'.format(
            download_dir, self.composer_id, self.work_id, self.page_id,
            self.track_id)

        utils.open_url(self.driver, host + '/secure/downloads.html')
        buttons = self.driver.find_elements_by_xpath(
            '//*[starts-with(@id,"dlBtn_")]//a')
        if len(buttons) != 1:
            utils.print_message('*ERROR*: {} download(s) available, '
                                '(check if not properly cleaned up or '
                                'reached daily limit.)'.format(len(buttons)))
            utils.print_message('*ERROR*: the next download is {}.mid'
                                .format(fname_prefix))
            return None

        size = buttons[0].find_element_by_xpath(
            '../../../../td[@class="dlSize"]').text.replace(' ','')
        url = buttons[0].get_attribute('href')
        basename = url.split('/')[-1]
        fname = '{}.size_{}.{}'.format(fname_prefix, size, basename)
        utils.download_file(url, fname)
        return fname


    def cleanup(self):

        utils.open_url(self.driver, host + '/secure/downloads.html',
                       reopen=True)
        utils.wait(3)

        self.driver.find_element_by_xpath(
            '//button[@onclick="return clearTracks()"]').click()
        utils.wait(3)

        confirms = self.driver.find_elements_by_xpath(
            '//*[@id="ConfDBox"]//button[@type="button"]')
        for confirm in confirms:
            if confirm.text == 'Yes':
                confirm.click()
                break
        utils.wait(3)

        buttons = self.driver.find_elements_by_xpath(
            '//*[starts-with(@id,"dlBtn_")]//a')
        return bool(len(buttons) == 0)


if __name__ == '__main__':

    import session
    import sys

    driver = utils.start_driver('chrome')
    home_dir = str(pathlib.Path.home())
    session.login(driver, home_dir + '/cma.credential.json')

    composer_id, work_id, page_id, track_id = [int(x) for x in
                                               sys.argv[1].split(',')]

    out_dir = 'midi/{}'.format(composer_id)
    job = Download(driver, composer_id, work_id, page_id, track_id)
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
    utils.wait(3)
    utils.close_driver(driver)
