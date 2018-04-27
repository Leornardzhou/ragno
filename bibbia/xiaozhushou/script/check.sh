#!/bin/bash

ts=$1

echo ":: check inconsistent number of vers"
for f in ../data/$ts/*.json; do
    echo $f $(python3 kit/print_json.py $f | grep vers | grep -v '""' | awk -F\" 'END{print NR,$4}')
done | awk 'NF==3 && $2!=$3'

echo ":: check content with character \* or \uff0a"
grep -c -e uff0a -e '\*' ../data/201804262332/*.json | grep -v :0$
