
## Prerequisits

Following GUI drivers are required in system `PATH` (e.g. `/usr/local/bin`)

* `geckodriver` [download page](https://github.com/mozilla/geckodriver/releases)
* `chromedriver` [download page](https://sites.google.com/a/chromium.org/chromedriver/downloads)
* `google-chrome-stable` (for ubuntu, in lieu of `chromedriver`)


## Procedures:

Get all composers in json format, output will be in data directory (`data/composers_[timestamp].json` and `data/composers_[timestamp].list`)

```bash
python3 script/get_all_composers.py 
```

Check if the number of MIDIs of each composer has changed (dependent on `data/composers_[timestamp].list`). *This may take a while.* If there are composers to be updated, the list (in csv format) will be show at the end.

```bash
python3 script_check_composer_online.py 
```


check integrity of DOWNLOADED composer json file (depend on composers.list) Expect to see no output.

```bash
python3 script_check_composer_local.py | awk '$2!=$3'
```

generate a list of all midis to download (depend on composers.list, compare with midi.list)

```bash
python3 script_generate_midi_list.py | sort > a
sort midi.list | diff - a
rm a
```


print json with key.subkey.subsubkey ...

```bash
python3 script_print_json.py xxx.json key.subkey.subsubkey[index]
```


get composer json, depend on composers.list (skip already existing), output = composer/xxx.json

``` bash
python3 script_get_composer.py
```


download midi given in midi.list (skip already existing) output = midi/xxx/xxx.mid, This command is part of crontab
```bash
python3 script_get_midi.py
```

## Other Tips:

To open GUI remotely, `DISPLAY=:0 (nohup) python3 xxx.py` or `export DISPLAY=:0`.
[reference](https://askubuntu.com/questions/47642/how-to-start-a-gui-software-on-a-remote-linux-pc-via-ssh)


## TODO:

* separate modules, scripts and data into different directories
* pylint check
* argparse

