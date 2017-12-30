import utils


search_url = 'https://app.pluralsight.com/library/search'


def get_filter_options_url(driver, filt_name):
    # filt_name = 'SKILL LEVELS', 'ROLES', 'SUBJECTS TO LEARN'
    # 'TOOLS', 'CERTIFICATIONS', 'AUTHORS'
    # reload the search url
    utils.print_message('get options of filter {} ...'.format(filt_name))
    utils.open_url(driver, search_url, reopen=True)

    opt_url_dict = dict()
    for filt in driver.find_elements_by_xpath(
            '//li[starts-with(@class, "facet__section ")]'):
        if filt_name != filt.find_element_by_xpath('./div/h3').text:
            continue

        # expand option list
        if (filt.get_attribute('class') ==
            'facet__section l-search__facets-list--item'):
            filt.find_element_by_xpath('./div/div').click()

        # get all options
        for opt in filt.find_elements_by_xpath('.//a[@role="checkbox"]'):
            opt_name= opt.get_attribute('aria-label')
            opt_url = opt.get_attribute('href')
            opt_url_dict[opt_name] = opt_url

    utils.print_message('found urls of {} options'.format(len(opt_url_dict)))

    return opt_url_dict


def get_all_courses_per_option(driver, opt_url, wait_time=5):

    utils.open_url(driver, opt_url, reopen=True, verbose=True)
    switch_to_courses(driver, 'Courses')
    ncourse = find_number_courses(driver)
    utils.print_message('loading {} courses'.format(ncourse))
    load_all_courses(driver, wait_time=wait_time)
    course_id_list = get_course_ids(driver)

    if ncourse != len(course_id_list):
        utils.print_message(
            '*ERROR*: number of courses mismatch, expected {}, loaded {}'
            .format(ncourse, len(course_id_list)))
        raise

    return course_id_list


def switch_to_courses(driver, tab_name):
    # tab_name = 'All', 'Courses', 'Paths'
    for tab in driver.find_elements_by_xpath(
            '//li[starts-with(@class, "tab-list__item")]'):
        if tab.text == tab_name:
            tab.click()
            break


def find_number_courses(driver):
    header = driver.find_element_by_xpath(
        '//span[starts-with(@class,"searchHeader---")]')
    try:
        ncourse = int(header.text.split()[1])
    except:
        ncourse = 0
    return ncourse


def load_all_courses(driver, wait_time=5):
    switch_to_courses(driver, 'Courses')
    while True:
        try:
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            driver.find_element_by_xpath(
                '//a[@class="button button--outlined"]').click()
            utils.wait(wait_time)
        except:
            break
    driver.execute_script("window.scrollTo(0, 0);")


def get_course_ids(driver):

    course_id_list = []
    for course in driver.find_elements_by_xpath(
            '//div[@class="l-search__results__primary"]/ol/div'):
        course_url = course.find_element_by_xpath(
            './/a[starts-with(@href, "/library/courses/")]')
        course_id = course_url.get_attribute('href').split('/')[-1]
        course_id_list.append(course_id)

    return course_id_list
