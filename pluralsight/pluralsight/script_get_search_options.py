import utils
import session
import search
import sys
import os
import pathlib


def get_search_options():

    driver = utils.start_driver('chrome')
    home_dir = str(pathlib.Path.home())
    session.login(driver, home_dir + '/plst.credential.json')
    utils.wait(3)

    filt_name_dict = {
        'level': 'SKILL LEVELS',
        'role': 'ROLES',
        'subject': 'SUBJECTS TO LEARN',
        'tool': 'TOOLS',
        'cert': 'CERTIFICATIONS',
        'author': 'AUTHORS',
    }

    try:

        for filt, filt_name in sorted(filt_name_dict.items()):
            opt_url_dict = search.get_filter_options_url(driver, filt_name)
            utils.save_json(opt_url_dict, 'search/filt_{}_urls.json'.format(filt))
            utils.wait(10)

    finally:
        session.logout(driver)
        utils.wait(3)
        utils.close_driver(driver)


get_search_options()



# load_course_video_list(sys.argv[1])
