import re
import json
from os.path import abspath, dirname
import sys
import gzip

root_dir = dirname(dirname(abspath(__file__)))
sys.path.append(root_dir)



field = None
json_name = sys.argv[1]

if len(sys.argv) == 3:
    field = sys.argv[2]

if json_name.endswith('.json.gz'):
    data = json.loads(gzip.open(json_name).read().decode('utf-8'))
else:
    data = json.loads(open(json_name).read())


if not field:

    print(json.dumps(data, sort_keys=True, indent=4, ensure_ascii=False))

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

    print(json.dumps(value, sort_keys=True, indent=4, ensure_ascii=False))
