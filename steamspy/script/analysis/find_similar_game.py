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


def load_tag_rank(tagrank_list):

    score_map = {
        0:0, 1:0, 2:1, 3:10, 4:100, 5:1000,
    }

    # score_map = {
    #     0:0, 1:0, 2:1, 3:2, 4:3, 5:4,
    # }

    tag_rank = dict()
    total_score = 0
    for line in open(tagrank_list):
        if line.startswith('标签'):
            continue
        index, name_en, name_cn, rank = line.rstrip().split(',')
        rank = int(rank)
        score = score_map[rank]
        total_score += score
        tag_rank[name_en] = score

    for tag in tag_rank:
        tag_rank[tag] /= total_score

    # for t,s in sorted(tag_rank.items(), key=lambda x: x[1], reverse=True):
    #     print(s, t)

    return tag_rank


def calc_tag_distance(in_json, tag_rank, out_list):

    data = json.loads(open(in_json).read())

    out = []
    print('reading ' + in_json)
    for appid in data:
        dist = 0
        norm = 0
        for tag in data[appid]['tags']:
            weight = tag_rank[tag.strip()]
            dist += weight*pow(data[appid]['tags'][tag] -
                               tag_rank[tag.strip()], 2)
        dist = math.sqrt(dist)
        out.append([appid, dist, data[appid]['nvote'], data[appid]['name']])

    print('writing ' + out_list)
    fout = open(out_list, 'w')
    for x in sorted(out, key=lambda x: x[1]):
        print('\t'.join(map(str,x)), file=fout)
    fout.close()


if __name__ == '__main__':

    # if len(sys.argv) != 4:
    #     print('Usage:\n  python3 calc_tag_distance.py  <timestamp>  '
    #           '<tag_rank>  <out_list>')
    #     sys.exit(0)

    # timestamp, tagrank_list, out_list = sys.argv[1:4]
    timestamp, tagrank_list, out_list = '201804010000', 'data/new_tags_score.csv', 'similar.list'

    data_dir = '../../data/{}/app'.format(timestamp)
    tagnorm_json = '{}.tagnorm.json'.format(timestamp)

    if not os.path.isfile(tagnorm_json):
        normalize_tag(data_dir, tagnorm_json)

    tag_rank = load_tag_rank(tagrank_list)

    calc_tag_distance(tagnorm_json, tag_rank, out_list)
