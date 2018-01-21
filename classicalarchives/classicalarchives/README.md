## Procedures:

get all composers, output = e.g. xxx.json, compare output with composers.json
```bash
python3 script_get_all_composers.py all.json
diff all.json composers.json
rm all.json
```

make composers.list (compare with composers.list)
```bash
python3 script_print_json.py composers.json | grep html | cut -d\" -f4 | awk -F\/ '{print $NF}' | sed 's/.html//g' | sort > a
sort composers.list | diff - a
rm a
```

# check if total number of midi changed online (dependent on
#  composers.list). This may take a while. If there are composers to be updated,
#  the list (in csv format) will be show at the end of stdout
$ python3 script_check_composer_online.py 



# check integrity of DOWNLOADED composer json file (depend on composers.list)
#  Expect to see no output.
$ python3 script_check_composer_local.py | awk '$2!=$3'



# generate a list of all midis to download (depend on composers.list, compare with midi.list)
$ python3 script_generate_midi_list.py | sort > a
$ sort midi.list | diff - a
$ rm a



# print json with key.subkey.subsubkey ...
$ python3 script_print_json.py xxx.json key.subkey.subsubkey[index]



# get composer json, depend on composers.list (skip already existing), output = composer/xxx.json
$ python3 script_get_composer.py



# download midi given in midi.list (skip already existing) output = midi/xxx/xxx.mid
#  This command is part of crontab
$ python3 script_get_midi.py


## Other Tips:

open GUI remotely
https://askubuntu.com/questions/47642/how-to-start-a-gui-software-on-a-remote-linux-pc-via-ssh
DISPLAY=:0 (nohup) python3 xxxx
or export DISPLAY=:0


need to have following GUI driver in PATH (e.g. /usr/local/bin)
geckodriver (https://github.com/mozilla/geckodriver/releases)
chromedriver (https://sites.google.com/a/chromium.org/chromedriver/downloads)
for linux, google-chrome-stable is used by webdriver (instead of chromedriver)
