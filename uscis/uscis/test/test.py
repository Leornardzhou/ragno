from os.path import abspath, dirname
package_path = dirname(dirname(dirname(abspath(__file__))))

import sys
sys.path.append(package_path)

from uscis import query


def test():

    receipt_number = sys.argv[1]
    status = query.query(receipt_number)
    print(status)


test()
