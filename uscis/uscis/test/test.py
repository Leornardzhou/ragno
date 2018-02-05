from os.path import abspath, dirname
package_path = dirname(dirname(dirname(abspath(__file__))))

import sys
sys.path.append(package_path)

from uscis import query
import json



def test():

    receipt_number_list = [
        'SRC1890055883',
        'SRC1890055884',
        'SRC1890055885',
        'SRC1890055886',
        'SRC1890055887',
        'SRC1890055888',
    ]
    status = query.query(receipt_number_list)
    for receipt_number, data in sorted(status.items()):
        print(receipt_number, json.dumps(data, sort_keys=True), sep='\t')


test()
