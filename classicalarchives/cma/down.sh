#!/bin/bash

# for c in $(awk 'NR>=101 && NR<=1000' composers.list); do
for c in $(cat composers.list); do
    if [ -f composer/$c.json ]; then
        continue
    fi
    echo $c
    # echo "---------------- $c ----------------"
    # python3 composer_debug.py $c composer/$c.json
    # echo
done


