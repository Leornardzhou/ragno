import os
import sys
import json
import math


def normalize_tag(data_dir, out_json):

    tag_set = set()
    app_dict = dict()
    for fname in os.listdir(data_dir):
        appid = fname.split('.')[0]
        fname = data_dir + '/' + fname
        data = json.loads(open(fname).read())
        if type(data['tags']) == list:
            data['tags'] = dict()
        app_dict[appid] = data
        for tag in data['tags']:
            tag_set.add(tag)

    ntag = len(tag_set)
    napp = len(app_dict)
    print('found {} tags, {} apps'.format(ntag, napp))

    # normalize tags in each app
    for appid, data in sorted(app_dict.items()):
        # add tags
        nvote = 0
        for tag in tag_set:
            if tag not in data['tags']:
                data['tags'][tag] = 0
            else:
                nvote += data['tags'][tag]
        data['nvote'] = nvote

        # normalize tag votes
        if nvote != 0:
            for tag in data['tags']:
                data['tags'][tag] /= nvote

    print('writing ' + out_json)
    fout = open(out_json, 'w')
    print(json.dumps(app_dict, sort_keys=True), file=fout)
    fout.close()




def calc_tag_distance(in_json, query_appid, out_list):

    data = json.loads(open(in_json).read())
    dist_measure = dict

    out = []
    print('reading ' + in_json)
    for appid in data:
        dist = 0
        norm = 0
        for tag in data[appid]['tags']:
            weight = data[query_appid]['tags'][tag]
            dist += weight*pow(data[appid]['tags'][tag] -
                               data[query_appid]['tags'][tag], 2)
        dist = math.sqrt(dist)
        out.append([appid, dist, data[appid]['nvote'], data[appid]['name']])

    print('writing ' + out_list)
    fout = open(out_list, 'w')
    for x in sorted(out, key=lambda x: x[1]):
        print('\t'.join(map(str,x)), file=fout)
    fout.close()


if __name__ == '__main__':

    if len(sys.argv) != 3:
        print('Usage:\n  python3 calc_tag_distance.py  <timestamp>  <appid>')
        sys.exit(0)

    timestamp, appid = sys.argv[1:3]

    data_dir = '../data/{}/app'.format(timestamp)
    tagnorm_json = '{}.tagnorm.json'.format(timestamp)

    if not os.path.isfile(tagnorm_json):
        normalize_tag(data_dir, tagnorm_json)

    dist_list = '{}.dist.{}.list'.format(timestamp, appid)
    calc_tag_distance(tagnorm_json, appid, dist_list)
