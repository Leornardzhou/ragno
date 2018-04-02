import os
import sys
import json



def get_tags(data_dir, timestamp):

    tag_dict = dict()
    json_dir = '{}/{}/app'.format(data_dir, timestamp)
    print('searching ' + json_dir, flush=True)
    for fname in os.listdir(json_dir):
        fname = json_dir + '/' + fname
        data = json.loads(open(fname).read())
        for x in data['tags']:
            if x not in tag_dict:
                tag_dict[x] = 0
            tag_dict[x] += 1

    return tag_dict


def main(data_dir, out_list):

    tag_dict = dict()
    for timestamp in sorted(os.listdir(data_dir)):
        if len(timestamp) == 12 and timestamp.startswith('2018'):
            tmp_tag_dict = get_tags(data_dir, timestamp)
            for x,n in tmp_tag_dict.items():
                if x not in tag_dict:
                    tag_dict[x] = 0
                tag_dict[x] += n

    fout = open(out_list, 'w')
    for x,n in sorted(tag_dict.items(), key=lambda x: x[1], reverse=True):
        print(n, x, sep='\t', file=fout)
    fout.close()


if __name__ == '__main__':

    main('../../data', 'all_tags.list')
