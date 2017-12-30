import sys
import json
import os
from os.path import join
import zipfile
import utils


def zip_size(course_zip):

    size = os.stat(course_zip).st_size
    if size == 0:
        print('*ERROR*: 0-byte zip file: {}'.format(course_zip))
    return size


def zip_content(course_name, course_zip):

    flist = zipfile.ZipFile(course_zip).namelist()
    nwrong = 0
    nright = 0
    for f in flist:
        if course_name not in f:
            nwrong += 1
        else:
            nright += 1
    if nwrong > 0:
        print('*ERROR*: wrong content ({} right {} wrong): {}'
              .format(nright, nwrong, course_zip))


def check_json(course_json):

    data = utils.load_json(course_json, verbose=False)
    # print([x for x in data])

    has_description = data['description']
    has_download = data['exercise_files']
    has_toc = data['table_of_content']
    has_transcript = data['transcript']
    # print(data['meta'])

    if has_toc and (data['table_of_content']['nmodule'] == 0 or
                    data['table_of_content']['nclip'] == 0):
        has_toc = False

    nmodule_nclip_mistmatch = False
    if (has_transcript and has_toc and (
            data['table_of_content']['nmodule'] != data['transcript']['nmodule'] or
            data['table_of_content']['nclip'] != data['transcript']['nclip']
    )):
        nmodule_nclip_mistmatch = True

    return [has_description, has_download, has_toc, has_transcript,
            nmodule_nclip_mistmatch]


def check_course():

    wrong_course_set = set()
    for course in sorted(os.listdir('courses')):

        course_dir = 'courses/{}'.format(course)

        course_json = '{}/{}.json'.format(course_dir, course)
        if not os.path.isfile(course_json):
            print('*ERROR*: missing json file: {}'.format(course_json))
            wrong_course_set.add(course)
            continue

        has_description, has_download, has_toc, has_transcript, \
            nmodule_nclip_mistmatch = check_json(course_json)

        if not has_description:
            print('*ERROR*: missing description: {}'.format(course_json))
            wrong_course_set.add(course)
            continue

        if not has_toc:
            print('*ERROR*: missing table of contents: {}'.format(course_json))
            wrong_course_set.add(course)
            continue

        if nmodule_nclip_mistmatch:
            print('*ERROR*: mismatch of #clips or #modules: {}'.format(course_json))
            wrong_course_set.add(course)
            continue

        # if not has_transcript:
        #     print('*ERROR*: missing transcript: {}'.format(course_json))
        #     continue

        course_zip = '{}/{}.zip'.format(course_dir, course)
        for f in os.listdir(course_dir):
            f = join(course_dir, f)
            if f.endswith('.zip') and f != course_zip:
                wrong_course_set.add(course)
                print('*ERROR*: wrong name of course zip: {}'.format(f))

        zip_exists = False
        if os.path.isfile(course_zip):
            size = zip_size(course_zip)
            zip_exists = True
            # zip_content(course, course_zip)

        if has_download and not zip_exists:
            wrong_course_set.add(course)
            print('*ERROR*: missing exercise files: {}'.format(course_json))
            continue

    for course in sorted(wrong_course_set):
        print(course)

check_course()
