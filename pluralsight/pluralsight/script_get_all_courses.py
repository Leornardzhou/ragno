import sys
import os
import json
import utils


def script_get_all_courses():

    course_set = set()
    for filt in ['role', 'subject', 'tool', 'cert']:
        filt_dir = 'search/filt_{}_courses'.format(filt)
        for fname in os.listdir(filt_dir):
            fname = '{}/{}'.format(filt_dir, fname)
            data = utils.load_json(fname, verbose=False)
            for option in data:
                for course in data[option]:
                    course_set.add(course)

    fout = open('courses.list', 'w')
    for course in sorted(course_set):
        print(course, file=fout)
    fout.close()


script_get_all_courses()
