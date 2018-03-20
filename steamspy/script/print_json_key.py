import sys
import json

data = json.loads(open(sys.argv[1]).read())
for x in sorted(data):
    print(x)
