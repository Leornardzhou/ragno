import re
import json
from os.path import abspath, dirname
import sys

root_dir = dirname(dirname(abspath(__file__)))
sys.path.append(root_dir)


from classicalarchives import utils


field = None
json_name = sys.argv[1]
if not json_name.endswith('.json'):
    json_name = 'courses/{}/{}.json'.format(json_name, json_name)

if len(sys.argv) == 3:
    field = sys.argv[2]

data = utils.load_json(json_name, verbose=False)

if not field:

    print(json.dumps(data, sort_keys=True, indent=4))

else:
    value = data
    for key in field.split('.'):
        index = -1
        if '[' in key and ']' in key:
            key, index = key.replace(']','').split('[')
            index = int(index)
        if index >= 0:
            value = value[key][index]
        else:
            value = value[key]

    print(json.dumps(value, sort_keys=True, indent=4))
