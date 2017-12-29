import utils
import course
import session
import sys
import os
import pathlib


def load_course_video_list(course_id):

    course_json = 'courses/{}/{}.json'.format(course_id, course_id)
    data = utils.load_json(course_json, verbose=False)

    nmodule = data['table_of_content']['nmodule']
    nclip = data['table_of_content']['nclip']
    video_list = []
    for module in data['table_of_content']['module_list']:
        module_id = module['module_id']
        for clip in module['clip_list']:
            clip_id = clip['clip_id']
            clip_url = clip['url']
            video_list.append([module_id, clip_id, clip_url])

    if nclip != len(video_list):
        utils.print_message('*ERROR*: course "{}", expected {} clips, found {}'
                            .format(course_id, nclip, len(video_list)))
        raise

    return video_list, nmodule, nclip


def count_videos(video_dir):

    nvideo = 0
    for fname in os.listdir(video_dir):
        if not (fname.endswith('.mp4') or fname.endswith('.webm')):
            continue
        nvideo += 1

    return nvideo


def get_course_videos(course_list, ncourse_max):

    cache_dir = 'cache'

    driver = utils.start_driver('chrome', download_dir=cache_dir)
    home_dir = str(pathlib.Path.home())
    session.login(driver, home_dir + '/plst.credential.json')
    utils.wait(3)

    try:
        ncourse = 0
        for line in open(course_list):
            if line.startswith('#'):
                continue
            course_id = line.rstrip()
            video_list, nmodule, nclip = load_course_video_list(course_id)
            nvideo = len(video_list)

            out_dir = 'courses/{}/videos'.format(course_id)
            os.makedirs(out_dir, exist_ok=True)

            if count_videos(out_dir) == nvideo:
                continue

            utils.print_message('get video of "{}" ({}/{}): {} modules and '
                                '{} clips'
                                .format(course_id, ncourse+1, ncourse_max,
                                        nmodule, nclip))

            for module_id, clip_id, clip_url in video_list:
                video_url = course.get_video_url(driver, clip_url)
                video_basename = video_url.split('?')[0].split('/')[-1]
                video_name = '{}/{}.{}.{}'.format(out_dir, module_id, clip_id,
                                                  video_basename)
                utils.download_file(video_url, video_name, verbose=True)


            ndownload = count_videos(out_dir)
            if ndownload != nvideo:
                utils.print_message('*ERROR*: course "{}", expected {} clips, '
                                    'downloaded {}'
                                    .format(course_id, nvideo, ndownload))
                raise

            ncourse += 1
            utils.print_message('----------------------------------------------')
            utils.wait(3)

            if ncourse == ncourse_max:
                break

    finally:
        session.logout(driver)
        utils.wait(3)
        utils.close_driver(driver)


# course_list = sys.argv[1]
ncourse_max = int(sys.argv[1])
course_list = 'courses.list'
get_course_videos(course_list, ncourse_max)



# load_course_video_list(sys.argv[1])
