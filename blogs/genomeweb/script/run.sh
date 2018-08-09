#!/bin/bash

ts=$(date +%Y%m%d%H)
python3 create_list.py $ts
python3 down_list.py $ts


