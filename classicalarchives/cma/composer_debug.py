'''This module works with /midi/composer/nnnn.html '''

import utils

host = 'https://www.classicalarchives.com'


class Composer:

    def __init__(self, driver, composer_id, verbose=False):
        url = host + '/midi/composer/{}.html'.format(composer_id)
        utils.open_url(driver, url, verbose=verbose)
        self.driver = driver
        self.composer_id = 'composer_{}'.format(composer_id)
        self.composer_url = url

        elem = self.driver.find_element_by_xpath('//h1[@class="composer"]')
        self.info = (elem.find_element_by_class_name('person_details').text)
        self.name = elem.text.replace(self.info, '').rstrip()
        self.ntrack = int(self.driver.find_element_by_xpath(
            '//div[@id="wMidi"]//li[@class="counts"]')
                          .text.split()[1].replace(',',''))
        self.nwork = len(self.driver.find_elements_by_xpath(
            '//*[@id="wMidi"]//a[starts-with(@id,"work_")]'))

        self.work_list = []


    def __str__(self):
        out = []
        out.append('composer_id = {}'.format(self.composer_id))
        out.append('composer_url = {}'.format(self.composer_url))
        out.append('name = {}'.format(self.name))
        out.append('info = {}'.format(self.info))
        out.append('nwork = {}'.format(self.nwork))
        out.append('ntrack = {}'.format(self.ntrack))
        return '\n'.join(out)


    def format_json(self, fname_out=None):
        data = {
            'composer_id': self.composer_id,
            'composer_url': self.composer_url,
            'name': self.name,
            'info': self.info,
            'nwork': self.nwork,
            'ntrack': self.ntrack,
        }
        data['work_list'] = []
        for work in self.work_list:
            data['work_list'].append(work.format_json())

        if fname_out:
            utils.save_json(data, fname_out)
        return data


    def get_work_by_id(self, work_id):
        work_elem = self.driver.find_element_by_xpath(
            '//div[@id="wMidi"]//a[@id="{}"]'.format(work_id))
        return Work(self.driver, work_elem)


    def get_all_works(self):
        nretry = 0
        work_list = []
        while True:

            work_list = []
            ntrack = 0
            work_elem_list = self.driver.find_elements_by_xpath(
                '//*[@id="wMidi"]//a[starts-with(@id,"work_")]')
            for work_elem in work_elem_list:
                work = Work(self.driver, work_elem)
                utils.print_message('get work {}'.format(work.title))
                work.get_all_pages()
                work_list.append(work)
                ntrack += work.ntrack
                work.collapse()

            if len(work_list) == self.nwork and ntrack == self.ntrack:
                break

            nretry += 1
            if len(work_list) != self.nwork:
                utils.print_message(
                    '*WARNING*: [{}] {} number of works mismatches, '
                    'expect {} found {}'
                    .format(self.composer_id, self.name, self.nwork,
                            len(self.work_list), nretry))
            if ntrack != self.ntrack:
                utils.print_message(
                    '*WARNING*: [{}] {} number of tracks mismatches, '
                    'expect {} found {}'
                    .format(self.composer_id, self.name, self.ntrack,
                            ntrack, nretry))
            if nretry == 20:
                sys.exit(1)

        self.work_list = work_list


class Work:

    def __init__(self, driver, work_elem):
        self.driver = driver
        self.work_elem = work_elem
        self.work_id = work_elem.get_attribute('id')
        self.title = self.work_elem.text
        self.ntrack = int(self.work_elem.find_element_by_xpath(
            '../div[@class="infolabel"]').text.split()[0].replace(',',''))

        self.expand()
        self.goto_page_by_name('last')
        self.npage = self.get_current_page_id()
        self.goto_page_by_name('first')
        utils.wait(2)  # allow time to update the page elements in the html
        self.page_list = []


    def __str__(self):
        out = []
        out.append('work_id = {}'.format(self.work_id))
        out.append('work_title = {}'.format(self.title))
        out.append('work_ntrack = {}'.format(self.ntrack))
        out.append('work_npage = {}'.format(self.npage))
        return '\n'.join(out)


    def format_json(self, fname_out=None):
        data = {
            'work_id': self.work_id,
            'title': self.title,
            'ntrack': self.ntrack,
            'npage': self.npage,
        }
        data['page_list'] = []
        for page in self.page_list:
            data['page_list'].append(page.format_json())

        if fname_out:
            utils.save_json(data, fname_out)
        return data


    def is_folded(self):
        toggle = self.work_elem.find_element_by_xpath(
            '..').get_attribute('class')
        return toggle == 'toggle'


    def expand(self):
        if self.is_folded():
            self.driver.execute_script("arguments[0].click();",
                                       self.work_elem)
            # self.work_elem.click()
            self.driver.execute_script("window.scrollBy(0, 200);")


    def collapse(self):
        if not self.is_folded():
            self.driver.execute_script("arguments[0].click();",
                                       self.work_elem)
            # self.work_elem.click()


    def goto_page_by_name(self, name):
        # name = first, previous, next, last
        page = self.work_elem.find_element_by_xpath(
            '..//*[@class="yui-pg-{}"]'.format(name))
        if page.tag_name == 'a':
            self.driver.execute_script("arguments[0].click();", page)
#            page.click()


    def goto_page_by_id(self, page_id):
        if page_id < 1 or page_id > self.npage:
            utils.print_message('*ERROR*: page_id {} exceeds limit [1,{}]'
                                .format(page_id, self.npage))
        current_page_id = self.get_current_page_id()
        if current_page_id < page_id:
            self.goto_page_by_name('next')
            while self.get_current_page_id() != page_id:
                self.goto_page_by_name('next')
        elif current_page_id > page_id:
            self.goto_page_by_name('previous')
            while self.get_current_page_id() != page_id:
                self.goto_page_by_name('previous')


    def get_current_page_id(self):
        current_page = self.work_elem.find_element_by_xpath(
            '..//*[@class="yui-pg-current-page yui-pg-page"]')
        return int(current_page.text)


    def get_current_page_elem(self):
        page_elem = self.work_elem.find_element_by_xpath(
            '..//*[@class="performance"]/..')
        return page_elem


    def get_page_by_id(self, page_id):
        self.goto_page_by_id(page_id)
        page_elem = self.get_current_page_elem()
        return Page(self.driver, page_elem)


    def get_all_pages(self):
        nretry = 0
        page_list = []
        while True:

            page_list = []
            ntrack = 0
            for i in range(self.npage):
                # self.goto_page_by_id(i+1)
                self.goto_page_by_name('next')
                utils.wait(2)  # allow time to update the page elements in the html
                page_elem = self.get_current_page_elem()
                utils.wait(2)  # allow time to update the page elements in the html
                page = Page(self.driver, page_elem)
                page.get_all_tracks()
                page_list.append(page)
                ntrack += page.ntrack

            if len(page_list) == self.npage and ntrack == self.ntrack:
                break

            nretry += 1
            if len(page_list) != self.npage:
                utils.print_message(
                    '*WARNING*: [{}] {} number of pages mismatches, '
                    'expect {} found {} (#retry = {})'
                    .format(self.work_id, self.title, self.npage,
                            len(page_list), nretry))
            if ntrack != self.ntrack:
                utils.print_message(
                    '*WARNING*: [{}] {} number of tracks mismatches, '
                    'expect {} found {} (#retry = {})'
                    .format(self.work_id, self.title, self.ntrack,
                            ntrack, nretry))
            if nretry == 20:
                sys.exit(1)

        self.page_list = page_list


class Page:

    def __init__(self, driver, page_elem):
        self.driver = driver
        self.page_elem = page_elem
        self.page_id = 'page_' + page_elem.find_element_by_xpath(
            '..//*[@class="yui-pg-current-page yui-pg-page"]').text
        self.contributor = page_elem.find_element_by_xpath(
            './/a[starts-with(@href, "/contributor/")]')
        self.contributor_url = self.contributor.get_attribute('href')
        self.contributor = self.contributor.text
        self.ntrack = int(self.page_elem.find_element_by_xpath(
            './/*[@class="buy"]/p').text.split()[0])
        self.length = self.page_elem.find_element_by_xpath(
            './/*[@class="play"]/*[@class="time"]').text
        self.track_list = []


    def __str__(self):
        out = []
        out.append('page_id = {}'.format(self.page_id))
        out.append('contributor = {}'.format(self.contributor))
        out.append('contributor_url = {}'.format(self.contributor_url))
        out.append('ntrack = {}'.format(self.ntrack))
        out.append('length = {}'.format(self.length))
        return '\n'.join(out)


    def format_json(self, fname_out=None):
        data = {
            'page_id': self.page_id,
            'contributor': self.contributor,
            'contributor_url': self.contributor_url,
            'ntrack': self.ntrack,
            'length': self.length,
        }
        data['track_list'] = []
        for track in self.track_list:
            data['track_list'].append(track.format_json())

        if fname_out:
            utils.save_json(data, fname_out)
        return data


    def get_all_tracks(self):

        track_list = []
        nretry = 0
        while True:

            track_list = []
            title_prefix = ''
            track_id = 1
            for elem in self.page_elem.find_elements_by_xpath('.//tbody/*'):
                is_header = False
                title = None
                length = None
                download_elem = None
                for subelem in elem.find_elements_by_xpath('./*'):
                    utils.wait(5)
                    if subelem.get_attribute('class') == 'tlEnd tlPart':
                        title_prefix = subelem.text + ' '
                        is_header = True
                    elif subelem.get_attribute('class') == 'tlTitle':
                        title = title_prefix + subelem.text
                    elif subelem.get_attribute('class') == 'tlLen':
                        length = subelem.text
                    elif subelem.get_attribute('class') == 'tlAdd':
                        download_elem = subelem
                if is_header:
                    continue
                track = Track(self.driver, track_id, title, length, download_elem)
                track_list.append(track)
                track_id += 1

            if len(track_list) == self.ntrack:
                break
            nretry += 1
            utils.print_message(
                '*WARNING*: [{}] {} number of tracks mismatches, '
                'expect {} found {} (#retry = {})'
                .format(self.page_id, self.contributor, self.ntrack,
                        len(track_list), nretry))
            if nretry == 20:
                sys.exit(1)

        self.track_list = track_list

    def get_track_by_id(self, track_id):
        # track_id = 1..ntrack (1-based)
        if len(self.track_list):
            return self.track_list[track_id-1]
        else:
            return None


class Track:

    def __init__(self, driver, track_id, title, length, download_elem):
        self.driver = driver
        self.track_id = 'track_{}'.format(track_id)
        self.title = title
        self.length = length
        self.download_elem = download_elem


    def download(self):
        self.driver.execute_script("arguments[0].click();",
                                   self.download_elem)
        # self.download_elem.click()


    def __str__(self):
        out = []
        out.append('title = {}'.format(self.title))
        out.append('length = {}'.format(self.length))
        return '\n'.join(out)


    def format_json(self, fname_out=None):
        data = {
            'track_id': self.track_id,
            'title': self.title,
            'length': self.length,
        }
        if fname_out:
            utils.save_json(data, fname_out)
        return data


if __name__ == '__main__':

    import sys

    composer_id = sys.argv[1]
    out_json = sys.argv[2]

    driver = utils.start_driver('phantomjs', wait_time=10)
    try:
        c = Composer(driver, composer_id)
        c.get_all_works()
        c.format_json(fname_out=out_json)

        # w = c.get_work_by_id('work_9458')
        # w.get_all_pages()
        # w.format_json(fname_out=out_json)

    except:
        utils.print_message('something is wrong.')
        raise
    finally:
        driver.close()
