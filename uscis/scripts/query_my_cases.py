'''This script retrieves the status of given receipt numbers and write
a status log file.
'''

import os
import sys
from os.path import abspath, dirname
root_dir = dirname(dirname(abspath(__file__)))
sys.path.append(root_dir)

from uscis import utils
from uscis.query import query
import json
from datetime import date, timedelta



def check_progress(log_today, log_yesterday):

    status_today = open(log_today).read()
    status_yesterday = open(log_today).read()

    if not os.path.isfile(log_yesterday):
        # today is the first day you run this.
        return

    if status_today != status_yesterday:
        utils.print_message('You have an update!!!')
        os.system('diff {} {}'.format(log_yesterday, log_today))

    else:
        utils.print_message('Sorry, nothing has changed.')



def query_my_case(receipt_number_list_name):

    timestamp_today = date.today().strftime("%Y%m%d")  # YYYYMMDD
    yesterday = date.today() - timedelta(1)
    timestamp_yesterday = yesterday.strftime("%Y%m%d")  # YYYYMMDD
    log_today = '{}/data/{}.status.log'.format(root_dir, timestamp_today)
    log_yesterday = '{}/data/{}.status.log'.format(root_dir, timestamp_yesterday)

    receipt_number_list = []
    for line in open(receipt_number_list_name):
        receipt_number_list.append(line.rstrip())

    status = query(receipt_number_list)

    utils.print_message('writing {}'.format(log_today))
    fout = open(log_today, 'w')
    for receipt_number, data in sorted(status.items()):
        print(receipt_number, json.dumps(data, sort_keys=True), sep='\t',
              file=fout)
    fout.close()

    check_progress(log_today, log_yesterday)


if __name__ == '__main__':

    receipt_number_list_name = sys.argv[1]
    query_my_case(receipt_number_list_name)
