import os
import sys
import json
from kit import utils




def print_csv_short_list():

    data = utils.load_json('../data/short_list/omim_diseases.json')

    fname_out = 'csv/omim_diseases.csv'
    utils.qprint('writing ' + fname_out)
    fout = open(fname_out, 'w')

    print('oid,name_cn,name_en', file=fout)
    for k,v in sorted(data.items()):
        print('OMIM:'+k, v['name_cn'].replace(',',''),
              v['name_en'].replace(',',''), sep=',', file=fout)
    fout.close()

def print_csv_full_data():

    fname_out = 'csv/full_list.csv'
    utils.qprint('writing ' + fname_out)
    fout = open(fname_out, 'w')

    print('oid,name_cn,name_en', file=fout)
    in_dir = '../data/full_data'
    for fname in sorted(os.listdir(in_dir)):
        oid_fname = fname.split('.')[1]
        db_type = None
        if fname.startswith('hp.'):
            db_type = 'HP'
        elif fname.startswith('omim.'):
            db_type = 'OMIM'
        fname = in_dir + '/' + fname
        data = utils.load_json(fname, verbose=False)

        oid, name_cn, name_en = None, None, None
        if db_type == 'HP':
            for x in data['results']:
                if x['hpoId'] != 'HP:' + oid_fname:
                    continue
                oid = x['hpoId']
                name_cn = ('{};{}'.format(x['name_cn'], x['definition_cn'])
                           .replace(',',''))
                name_en = ('{};{}'.format(x['name_en'], x['definition_en'])
                           .replace(',',''))

        elif db_type == 'OMIM':
            for x in data['results']:
                if str(x['mimNumber']) != oid_fname:
                    continue
                oid = 'OMIM:' + str(x['mimNumber'])
                name_cn = x['cnTitle'].replace(',','')
                name_en = x['preTitle'].replace(',','')

        if oid:
            print(oid, name_cn, name_en, sep=',', file=fout)

    fout.close()

if __name__ == '__main__':

    print_csv_short_list()
    print_csv_full_data()
