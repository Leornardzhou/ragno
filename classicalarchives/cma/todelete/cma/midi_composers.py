import sys

def get_all_composers_with_initial(session, initial):
    ''' get data of all composers starting with initial '''

    result = []
    url = session.domain + '/midi/composers/{}.html'.format(initial)
    sess.open_url(url)
    debug_print('')
    composer_list = sess.driver.find_elements_by_xpath('//a[starts-with(@href,'
