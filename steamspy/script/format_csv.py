'''Generate a csv file containing all games and properties.
'''

import os
from os.path import join
import sys
import json


def load_genre(data_dir):

    print('reading all genres', file=sys.stderr, flush=True)
    genre_dir = '{}/genre'.format(data_dir)
    genre_dict = dict()
    for fname in os.listdir(genre_dir):
        genre = fname.split('.')[0]
        fname = join(genre_dir, fname)
        data = json.loads(open(fname).read())
        for appid in data:
            if appid not in genre_dict:
                genre_dict[appid] = set()
            genre_dict[appid].add(genre)

    return genre_dict



def make_csv(data_dir, csv_out):

    app_dir = '{}/app'.format(data_dir)
    genre_dict = load_genre(data_dir)
    delimiter = ','

    # missing release date, genre is not complete

    csv_keys = [
        'appid', 'name', 'developer', 'publisher', 'price', 'tags', 'genres',
        'score_rank', 'positive', 'negative', 'userscore',
        'owners', 'owners_variance',
        'players_2weeks', 'players_2weeks_variance',
        'players_forever', 'players_forever_variance',
        'ccu', 'average_2weeks', 'average_forever',
        'median_2weeks', 'median_forever',
    ]

    print('reading all app details', file=sys.stderr, flush=True)
    print('writing ' + csv_out, file=sys.stderr, flush=True)
    fout = open(csv_out, 'w')
    print(delimiter.join(csv_keys), file=fout)
    for fname in os.listdir(app_dir):
        appid = fname.split('.')[0]
        fname = join(app_dir, fname)
        data = json.loads(open(fname).read())
        out = []
        for key in csv_keys:
            if key == 'tags':
                tag_delimiter = ':'
                tags_list = sorted(data[key], key=lambda x: data[key][x],
                                   reverse=True)
                out.append('{}{}{}'.format(
                    tag_delimiter, tag_delimiter.join(tags_list),
                    tag_delimiter))
            elif key == 'genres':
                genre_delimiter = '@'
                if appid in genre_dict:
                    genres_list = sorted(genre_dict[appid])
                else:
                    genres_list = []
                out.append('{}{}{}'.format(
                    genre_delimiter, genre_delimiter.join(genres_list),
                    genre_delimiter))
            else:
                out.append(str(data[key]).replace(delimiter, ';'))
        print(delimiter.join(out), file=fout)
    fout.close()


if __name__ == '__main__':

    if len(sys.argv) != 3:
        print('Usage:   python3 format_csv.py  <data_dir>  <csv_out>')
        sys.exit(0)

    data_dir, csv_out = sys.argv[1:3]
    make_csv(data_dir, csv_out)
