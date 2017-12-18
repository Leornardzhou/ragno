import sys
import json
import utils


json_name = sys.argv[1]
data = utils.load_json(json_name)
print(json.dumps(data, sort_keys=True, indent=4))
