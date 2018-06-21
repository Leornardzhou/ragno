#!/bin/bash

home="$( cd "$( dirname "${BASH_SOURCE[0]}" )/../" && pwd )"
python3 $home/script/proxydocker.py 50

