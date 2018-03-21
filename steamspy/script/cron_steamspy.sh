#!/bin/bash -e

home="$( cd "$( dirname "${BASH_SOURCE[0]}" )/../" && pwd )"

timestamp=$(date +%Y%m%d%H%M)

out_dir=$home/data/$timestamp
mkdir -p $out_dir
log=$out_dir/$timestamp.log
csv=$out_dir/$timestamp.csv

proxy_dir=$home/../proxy/data_valid

echo python3 $home/script/get_data_via_api.py $proxy_dir $out_dir 
python3 $home/script/get_data_via_api.py $proxy_dir $out_dir &> $log

echo python3 $home/script/format_csv.py $out_dir $csv &>> $log
python3 $home/script/format_csv.py $out_dir $csv &>> $log


# wrap up
cd $home/data/

echo gzip $log
gzip $log

echo gzip $csv
gzip $csv

echo tar cvzf $timestamp.tar.gz $timestamp
tar cvzf $timestamp.tar.gz $timestamp
rm -r $timestamp

cd

