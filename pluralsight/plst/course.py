import sys
import utils
import os


host = 'https://app.pluralsight.com'

def click_wootric_x(driver):

    dismiss = driver.find_elements_by_xpath('wootric-x')
    if len(dismiss):
        dismiss[0].click()
        self.driver.execute_script("window.scrollTo(0, 0);")


class Course:

    def __init__(self, driver, cache_dir, course_id):
        # course_id e.g. embedded-systems-programming

        self.driver = driver
        self.cache_dir = cache_dir

        course_url = host + '/library/courses/' + course_id
        utils.open_url(driver, course_url)
        click_wootric_x(driver)

        self.meta = CourseMeta(driver, course_url, course_id)

        self.table_of_content = None
        self.transcript = None

        self.description = None
        self.exercise_files = None


    def __str__(self):

        out = []
        out.append('meta: \n{}\n'.format(str(self.meta)))
        out.append('description: \n{}\n'.format(self.description))
        out.append('exercise_files: {}\n'.format(self.exercise_files))
        out.append('table of content: \n{}\n'.format(
            str(self.table_of_content)))
        out.append('transcript: \n{}\n'.format(
            str(self.transcript)))
        return '\n'.join(out)


    def format_json(self, fname=None):

        out = {}
        out['meta'] = self.meta.format_json()
        out['description'] = self.description
        out['exercise_files'] = self.exercise_files
        out['table_of_content'] = (self.table_of_content.format_json()
                                   if self.table_of_content else None)
        out['transcript'] = (self.transcript.format_json()
                             if self.transcript else None)

        if fname:
            utils.save_json(out, fname)

        return out


    def switch_tab(self, tab_name):

        self.driver.execute_script("window.scrollTo(0, 0);")
        tab_list = self.driver.find_elements_by_xpath(
            '//*[starts-with(@class,"tab-list__item")]')
        for tab in tab_list:
            if tab.text == tab_name:
                tab.click()
                click_wootric_x(self.driver)
                return True
        return False  # no such tab found


    def get_description(self):

        if not self.switch_tab('Description'):
            utils.print_message('This course has no description.')
            return

        utils.print_message('extracting description ...')
        self.description = self.driver.find_element_by_xpath(
            '//div[@class="l-course-page__content"]/p').text


    def get_exercise_files(self, down_dir):

        if not self.switch_tab('Exercise files'):
            utils.print_message('This course has no exercise files.')
            return

        button_list = self.driver.find_elements_by_xpath(
            '//button[@class="button"]')

        if len(button_list) == 0:
            utils.print_message('This course has no exercise files.')
            return

        for button in button_list:
            if button.text != 'Download exercise files':
                continue
            utils.print_message('downloading exercise files ...')
            button.click()
            self.exercise_files = self.rename_exercise_files(down_dir)


    def rename_exercise_files(self, down_dir):

        # get downloaded temporary file
        tmp_fname = ''
        while True:
            tmp_flist = [self.cache_dir + '/' + x
                              for x in os.listdir(self.cache_dir)
                         if x.endswith('.zip')]

            if len(tmp_flist) != 0:
                tmp_flist.sort(key=lambda x: os.path.getmtime(x),
                               reverse=True)
                tmp_fname = tmp_flist[0]
                break

            utils.wait(3)

        os.makedirs(down_dir, exist_ok=True)
        new_fname = '{}/{}'.format(down_dir, tmp_fname.split('/')[-1])
        os.rename(tmp_fname, new_fname)
        utils.print_message('save downloaded exercise files as {}'
                            .format(new_fname))
        return new_fname


    def get_transcript(self):

        if not self.switch_tab('Transcript'):
            utils.print_message('This course has no transcript.')
            return

        utils.print_message('extracting transcript ...')

        self.transcript = Transcript(self.driver)
        utils.print_message('found {} modules and {} clips'
                            .format(self.transcript.nmodule,
                                    self.transcript.nclip))


    def get_table_of_content(self):

        if not self.switch_tab('Table of contents'):
            utils.print_message('This course has no table of contents.')
            return

        utils.print_message('extracting table of content ...')

        # expand all
        expand = self.driver.find_element_by_xpath(
            '//a[@class="accordian__action"]')
        if expand.text == 'Expand all':
            yloc = expand.location['y'] - 100
            self.driver.execute_script("window.scrollTo(0, {});".format(yloc))
            expand.click()

        # get table of content
        self.table_of_content = TableOfContent(self.driver)

        utils.print_message('found {} modules and {} clips'
                            .format(self.table_of_content.nmodule,
                                    self.table_of_content.nclip))


class CourseMeta:

    def __init__(self, driver, course_url, course_id):
        self.driver = driver
        self.course_url = course_url
        self.course_id = course_id

        self.course_name = self.driver.find_element_by_xpath(
            '//h1[@class="course-hero__title"]').text

        self.course_intro = self.driver.find_element_by_xpath(
            '//p[@class="course-hero__excerpt"]').text

        self.author_list = []
        for elem in self.driver.find_elements_by_xpath(
                '//*[@class="author-tease__name"]'):
            self.author_list.append(elem.text)

        self.level = None
        self.length = None
        self.date = None
        self.rating = None
        for elem in self.driver.find_elements_by_xpath(
                '//li[@class="detail-list__item"]'):
            title = elem.find_element_by_xpath(
                './span[@class="detail-list__title"]').text
            desc = elem.find_element_by_xpath(
                './span[@class="detail-list__desc"]')
            if title == 'Level':
                self.level = desc.text
            elif title == 'Duration':
                self.length = desc.text
            elif title == 'Released':
                self.date = desc.text
            elif title == 'Updated':
                self.date = desc.text
            elif title == 'Rating':
                self.rating = (desc.find_element_by_xpath('./div')
                               .get_attribute('aria-label'))

        # get course path if available
        self.path = None
        path_list = self.driver.find_elements_by_xpath(
            '//a[@class="table-of-contents__skill-path-link"]')
        if len(path_list) != 0:
            self.path = path_list[0].text


    def __str__(self):

        out = []
        out.append('course_id: {}'.format(self.course_id))
        out.append('course_url: {}'.format(self.course_url))
        out.append('course_name: {}'.format(self.course_name))
        out.append('author_list: {}'.format(','.join(self.author_list)))
        out.append('course_intro: {}'.format(self.course_intro))
        out.append('level: {}'.format(self.level))
        out.append('length: {}'.format(self.length))
        out.append('date: {}'.format(self.date))
        out.append('rating: {}'.format(self.rating))
        out.append('path: {}'.format(self.path))
        return '\n'.join(out)


    def format_json(self):

        out = {}
        out['course_id'] = self.course_id
        out['course_url'] = self.course_url
        out['course_name'] = self.course_name
        out['course_intro'] = self.course_intro
        out['author_list'] = self.author_list
        out['level'] = self.level
        out['length'] = self.length
        out['date'] = self.date
        out['rating'] = self.rating
        out['path'] = self.path
        return out

# =============================================================================

class Transcript:


    def __init__(self, driver):

        self.driver = driver
        self.nmodule = 0
        self.nclip = 0
        self.module_list = []
        self.load_all_modules()


    def load_all_modules(self):

        module_id = 1
        for module_elem in self.driver.find_elements_by_xpath(
                '//div[@class="course-transcript__module"]'):
            module = TranscriptModule(module_elem, module_id)
            self.module_list.append(module)
            self.nmodule += 1
            self.nclip += module.nclip
            module_id += 1


    def __str__(self):

        out = []
        out.append('nmodule: {}'.format(self.nmodule))
        out.append('nclip: {}'.format(self.nclip))
        out.append('modules: \n{}'.format('\n'.join([str(a)
                                                for a in self.module_list])))
        return '\n'.join(out)


    def format_json(self):

        out = {}
        out['nmodule'] = self.nmodule
        out['nclip'] = self.nclip
        out['module_list'] = [x.format_json() for x in self.module_list]
        return out


class TranscriptModule:


    def __init__(self, module_elem, module_id):

        self.module_elem = module_elem
        self.module_id = module_id
        self.title = module_elem.find_element_by_xpath(
            './h2[@class="course-transcript__module-header"]/a').text
        self.nclip = 0
        self.clip_list = []
        self.load_all_clips()


    def load_all_clips(self):

        clip_id = 1
        for clip_elem in self.module_elem.find_elements_by_xpath('./div'):
            clip = TranscriptClip(clip_elem, clip_id)
            self.clip_list.append(clip)
            self.nclip += 1
            clip_id += 1


    def __str__(self):

        out = []
        out.append('module_id: {}'.format(self.module_id))
        out.append('title: {}'.format(self.title))
        out.append('nclip: {}'.format(self.nclip))
        out.append('clips: \n{}'.format('\n'.join([str(a)
                                                for a in self.clip_list])))
        return '\n'.join(out)


    def format_json(self):

        out = {}
        out['module_id'] = self.module_id
        out['title'] = self.title
        out['nclip'] = self.nclip
        out['clip_list'] = [x.format_json() for x in self.clip_list]
        return out


class TranscriptClip:


    def __init__(self, clip_elem, clip_id):

        self.clip_elem = clip_elem
        self.clip_id = clip_id
        self.title = clip_elem.find_element_by_xpath(
            './h3[@class="course-transcript__clip-header"]/a').text
        self.nline = 0
        self.line_list = []
        self.load_all_lines()


    def load_all_lines(self):

        line_id = 1
        for line_elem in self.clip_elem.find_elements_by_xpath('./p/span/a'):
            line = TranscriptLine(line_elem, line_id)
            self.line_list.append(line)
            self.nline += 1
            line_id += 1


    def __str__(self):

        out = []
        out.append('clip_id: {}'.format(self.clip_id))
        out.append('title: {}'.format(self.title))
        out.append('nline: {}'.format(self.nline))
        out.append('lines: \n{}'.format(' '.join([str(a)
                                                for a in self.line_list])))
        return '\n'.join(out)


    def format_json(self):

        out = {}
        out['clip_id'] = self.clip_id
        out['title'] = self.title
        out['nline'] = self.nline
        out['line_list'] = [x.format_json() for x in self.line_list]
        return out


class TranscriptLine:


    def __init__(self, line_elem, line_id):
        self.line_elem = line_elem
        self.line_id = line_id
        self.content = line_elem.text
        self.timestamp = line_elem.get_attribute('href').split('=')[-1]


    def __str__(self):
        return self.content


    def format_json(self):
        out = {}
        out['line_id'] = self.line_id
        out['content'] = self.content
        out['timestamp'] = self.timestamp
        return out

# =============================================================================

class TableOfContent:

    def __init__(self, driver):

        self.driver = driver
        self.nmodule = 0
        self.nclip = 0
        self.module_list = []
        self.load_all_modules()


    def load_all_modules(self):

        module_id = 1
        for module_elem in self.driver.find_elements_by_xpath(
                '//li[@class="accordian__section accordian__section--open"]'):
            module = TableOfContentModule(module_elem, module_id)
            self.module_list.append(module)
            self.nmodule += 1
            self.nclip += module.nclip
            module_id += 1


    def __str__(self):

        out = []
        out.append('nmodule: {}'.format(self.nmodule))
        out.append('nclip: {}'.format(self.nclip))
        out.append('modules: \n{}'.format(
            '\n'.join([str(x) for x in self.module_list])))
        return '\n'.join(out)


    def format_json(self):

        out = {}
        out['nmodule'] = self.nmodule
        out['nclip'] = self.nclip
        out['module_list'] = [module.format_json()
                              for module in self.module_list]
        return out


class TableOfContentModule:


    def __init__(self, module_elem, module_id):

        self.module_elem = module_elem
        self.module_id = 'module_{}'.format(module_id)
        self.title = module_elem.find_element_by_xpath(
            './/h3[@class="table-of-contents__title"]/a').text
        self.length = module_elem.find_element_by_xpath(
            './/time[@class="table-of-contents__time"]').text
        self.nclip = 0
        self.clip_list = []
        self.load_all_clips()


    def load_all_clips(self):

        clip_id = 1
        for clip_elem in self.module_elem.find_elements_by_xpath(
                './/li[@class="table-of-contents__clip-list-item"]'):
            clip = TableOfContentClip(clip_elem, clip_id)
            self.clip_list.append(clip)
            self.nclip += 1
            clip_id += 1


    def __str__(self):

        out = []
        out.append('module_id: {}'.format(self.module_id))
        out.append('title: {}'.format(self.title))
        out.append('length: {}'.format(self.length))
        out.append('nclip: {}'.format(self.nclip))
        out.append('clips: \n{}'.format(
            '\n'.join([str(x) for x in self.clip_list])))
        return '\n'.join(out)


    def format_json(self):

        out = {}
        out['module_id'] = self.module_id
        out['title'] = self.title
        out['length'] = self.length
        out['nclip'] = self.nclip
        out['clip_list'] = [clip.format_json() for clip in self.clip_list]
        return out


class TableOfContentClip:


    def __init__(self, clip_elem, clip_id):

        self.clip_elem = clip_elem
        self.clip_id = 'clip_{}'.format(clip_id)
        clip = clip_elem.find_element_by_xpath('./a')
        self.title = clip.text
        self.url = clip.get_attribute('href')
        self.length = clip_elem.find_element_by_xpath(
            './/time[@class="table-of-contents__time"]').text


    def __str__(self):

        out = []
        out.append('clip_id: {}'.format(self.clip_id))
        out.append('title: {}'.format(self.title))
        out.append('length: {}'.format(self.length))
        out.append('url: {}'.format(self.url))
        return '\n'.join(out)


    def format_json(self):

        out = {}
        out['clip_id'] = self.clip_id
        out['title'] = self.title
        out['length'] = self.length
        out['url'] = self.url
        return out
