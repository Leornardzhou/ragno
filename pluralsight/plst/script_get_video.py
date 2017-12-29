import utils
import course
import session
import sys
import os
import pathlib


def load_course_json(course_id):

    course_json = 'courses/{}/{}.json'.format(course_id, course_id)
    data = utils.load_json(course_json)

    nmodule = data['table_of_content']['nmodule']
    nclip = data['table_of_content']['nclip']
    url_list = []
    for module in data['table_of_content']['module_list']:
        module_id = module['module_id']
        for clip in module['clip_list']:
            clip_id = clip['clip_id']
            clip_url = clip['clip_url']
            url_list.append([module_id, clip_id, clip_url])

    if nclip != len(clip_list):
        utils.print_message('*ERROR*: course "{}", expected {} clips, found {}'
                            .format(course_json, nclip, len(clip_list)))
        sys.exit(1)

    return url_list



def get_videos(ncourse_max):

    cache_dir = 'cache'

    driver = utils.start_driver('chrome', download_dir=cache_dir)
    home_dir = str(pathlib.Path.home())
    session.login(driver, home_dir + '/plst.credential.json')
    utils.wait(3)

    try:
        ncourse = 0
        for line in open('courses.list'):
            if line.startswith('#'):
                continue
            course_id = line.rstrip()
            out_dir = 'courses/' + course_id
            fname_json = '{}/{}.json'.format(out_dir, course_id)
            if os.path.isfile(fname_json):
                continue
            utils.print_message('get course "{}" ({}/{})'.format(course_id, ncourse+1, ncourse_max))
            c = course.Course(driver, cache_dir=cache_dir, course_id=course_id)
            c.get_description()
            c.get_exercise_files(out_dir)
            c.get_table_of_content()
            c.get_transcript()
            c.format_json(fname_json)
            ncourse += 1
            utils.print_message('----------------------------------------------')
            utils.wait(3)

            if ncourse == ncourse_max:
                break
    finally:
        session.logout(driver)
        utils.wait(3)
        utils.close_driver(driver)


# ncourse_max = int(sys.argv[1])
# get_course(ncourse_max)



load_course_json(sys.argv[1])
