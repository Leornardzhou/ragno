import utils
import session
import search
import sys
import os
import pathlib
import re


def get_search_option_courses():

    driver = utils.start_driver('chrome')
    home_dir = str(pathlib.Path.home())
    session.login(driver, home_dir + '/plst.credential.json')
    utils.wait(3)

    filt_name_dict = {
        'role': 'ROLES',
        'subject': 'SUBJECTS TO LEARN',
        'tool': 'TOOLS',
        'cert': 'CERTIFICATIONS',
        'level': 'SKILL LEVELS',
        'author': 'AUTHORS',
    }

    try:

        for filt, filt_name in sorted(filt_name_dict.items()):
            opt_url_dict = utils.load_json(
                'search/filt_{}_urls.json'.format(filt))
            out_dir = 'search/filt_{}_courses'.format(filt)
            os.makedirs(out_dir, exist_ok=True)

            opt_index = 0
            nopt = len(opt_url_dict)
            for opt, url in sorted(opt_url_dict.items()):
                opt_index += 1
                fname_json = '{}/{}.json'.format(out_dir, opt_index)
                if os.path.isfile(fname_json):
                    continue
                # if opt_index >= 10:
                #     break
                utils.print_message(
                    'get all courses with filt={}, option={} ({}/{})'
                    .format(filt, opt, opt_index, nopt))
                course_id_list = search.get_all_courses_per_option(
                    driver, url, wait_time=10)
                opt_courses_dict = {opt: course_id_list}
                utils.save_json(opt_courses_dict, fname_json)
                utils.wait(20)

    finally:
        session.logout(driver)
        utils.wait(3)
        utils.close_driver(driver)


get_search_option_courses()



# load_course_video_list(sys.argv[1])
