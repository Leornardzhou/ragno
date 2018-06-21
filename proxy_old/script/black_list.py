'''This program create a list of proxies which are not effectively changing ip.
'''

import os
import json
import gzip
import sys
import requests
from os.path import dirname, abspath

root_dir = dirname(dirname(abspath(__file__)))
data_dir = '{}/data'.format(root_dir)

def black_list(json_name, out_bl_name):


    r = requests.get('http://icanhazip.com')
    here = r.text.rstrip().rsplit('.',2)[0] + '.'

    print('reading '+json_name)
    data = json.loads(gzip.open(json_name).read().decode('utf-8'))

    blist = set()
    ndata = len(data)
    for i,x in enumerate(sorted(data)):
        print('testing proxy ({}/{}) {} ... '
              .format(i+1, ndata, x), end='', flush=True)
        try:
            r = requests.get('http://icanhazip.com', proxies={'http':x},
                             timeout=(0.1, 0.1))
            if r.text.startswith(here):
                print('black!', end='', flush=True)
                blist.add(x)
        except:
            pass
        print(flush=True)

    print('writing ' + out_bl_name)
    fout = open(out_bl_name, 'w')
    for x in sorted(blist):
        print(x, file=fout)
    fout.close()


if __name__ == '__main__':

    for fin in sorted(os.listdir(data_dir)):
        if fin.endswith('.proxies.json.gz') and fin.startswith('proxydocker'):
            timestamp = fin.split('.')[1]
            out_bl_name = ('{}/proxydocker.{}.proxies.blacklist'
                           .format(data_dir, timestamp))
            fin = data_dir + '/' + fin
            if os.path.isfile(out_bl_name):
                continue
            black_list(fin, out_bl_name)
            print()
