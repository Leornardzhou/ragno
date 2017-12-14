import utils
import json
import sys


composer_json = sys.argv[1]
composer = utils.load_json(composer_json, verbose=False)

ntrack = 0
for work in composer['work_list']:
    ntrack_work = 0
    for page in work['page_list']:
        ntrack_page = 0
        for track in page['track_list']:
            ntrack += 1
            ntrack_page += 1
            ntrack_work += 1
    #     if ntrack_page != page['ntrack']:
    #         print('work {} page {} {}'.format(work['title'],
    #                                           page['contributor'],
    #                                           page['page_id']))
    # if ntrack_work != work['ntrack']:
    #     print('work {}'.format(work['title']))
    #     print(json.dumps(work, sort_keys=True, indent=4))

print(composer_json, composer['ntrack'], ntrack)
