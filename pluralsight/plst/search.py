import utils
import session
import sys
import imp
import time


host = 'https://app.pluralsight.com'


def load_all_courses(driver, html_name, num_load=None):

    utils.open_url(driver, host + '/library/search')

    # switch to Course tab
    for elem in driver.find_elements_by_xpath('//li[@class="tab-list__item"]'):
        if elem.text == 'Courses':
            elem.click()

    # define target scraping section
    course_section = driver.find_element_by_xpath(
        '//div[@aria-selected="true"]')

    # expected number
    ncourse_expect = int(course_section.find_element_by_xpath(
        './/*[@class="l-search__results-page-info"]').text.split()[1])

    nload = 0
    if num_load:
        nload_max = num_load
    else:
        nload_max = (ncourse_expect // 25) + 3

    while nload < nload_max:
        courses = course_section.find_elements_by_xpath(
            './/li[@class="courses-list__item"]')
        ncourses = len(courses)
        utils.print_message('#load={}, ncourses={}'.format(nload, ncourses))

        nload += 1
        buttons = course_section.find_elements_by_xpath(
            './/a[@class="button button--outlined"]')
        if len(buttons) == 0:
            break

        buttons[0].click()
        utils.wait(3)

    # save html
    utils.save_html(driver, html_name)

    course_list = course_section.find_elements_by_xpath(
        './/li[@class="courses-list__item"]')
    utils.print_message('expect {} courses, loaded {}.'.format(
        ncourse_expect, len(course_list)))


def get_all_courses(driver, json_name):

    course_section = driver.find_element_by_xpath(
        '//div[@aria-selected="true"]')
    course_list = course_section.find_elements_by_xpath(
        './/li[@class="courses-list__item"]')

    out_list = []
    ncourse = 0
    for course in course_list:
        out = {}
        course_header = course.find_element_by_xpath(
            './/*[@class="courses-list__item-headers"]/a')
        out['title'] = course_header.get_attribute('title')
        out['url'] = course_header.get_attribute('href')
        course_meta = course.find_element_by_xpath(
            './/*[@class="courses-list__item-meta"]')
        out['author'] = course_meta.find_element_by_xpath(
            './p[@class="courses-list__item-authors"]/span/a').text
        out['level'] = course_meta.find_element_by_xpath(
            './p[@class="courses-list__item-level"]').text
        out['date'] = course_meta.find_element_by_xpath(
            './time[@class="courses-list__item-date"]').text
        out['level'] = course_meta.find_element_by_xpath(
            './time[@class="courses-list__item-duration"]').text
        ncourse += 1
        out_list.append(out)

    utils.save_json(out_list, json_name)


if __name__ == '__main__':

    import session

    driver = utils.start_driver('chrome')
    out_json = sys.argv[1]
    out_html = out_json.rsplit('.',1)[0] + '.html'
    try:
        session.login(driver, 'input/credential.json')
        load_all_courses(driver, out_html, num_load=None)
        get_all_courses(driver, out_json)

    finally:
        utils.close_driver(driver)
