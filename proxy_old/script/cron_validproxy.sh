#!/bin/bash

home="$( cd "$( dirname "${BASH_SOURCE[0]}" )/../" && pwd )"

# python3 $home/script/black_list.py

python3 $home/script/verify_proxy.py $home/data_valid
