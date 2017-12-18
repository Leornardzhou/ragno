import utils

data = utils.load_json('search/all_courses.json')
print(len(data))
for x in data:
    print(x)
