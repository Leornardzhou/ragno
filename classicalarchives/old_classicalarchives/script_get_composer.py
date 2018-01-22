import composer
import utils
import sys
import os

todo_list = 'composers.list'

driver = utils.start_driver('chrome', wait_time=5)

for composer_id in open(todo_list):
    composer_id = composer_id.rstrip()
    try:
        out_json = 'composer/{}.json'.format(composer_id)
        if os.path.isfile(out_json):
            # print(out_json + ' is already there, skip.')
            continue
        c = composer.Composer(driver, composer_id)
        c.get_all_works()
        c.format_json(fname_out=out_json)
        utils.print_message('\n\n\n')

    except:
        # raise
        e = sys.exc_info()[0]
        utils.print_message('something is wrong.\n{}\n\n\n'.format(str(e)))
    # break

driver.close()
