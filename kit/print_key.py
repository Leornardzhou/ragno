import sys
import json
import gzip

json_name = sys.argv[1]
if json_name.endswith('.gz'):
    data = json.loads(gzip.open(json_name).read().decode('utf-8'))
else:
    data = json.loads(open(json_name).read())

for x in sorted(data):
    print(x)
