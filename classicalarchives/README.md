This package automates the MIDI download from [ClassicalArchives](https://www.classicalarchives.com/). You will need a valid premium account to download the data. The scripts provided below allow you to download maximum number of MIDIs (per day) set by the website.


### Prerequisites

The package requires Selenium (tested version 3.8.0) and Python Virtual Display (tested version 0.2.1) for remote cron jobs. These packages can be installed using 

```bash
pip3 install -U selenium PyVirtualDisplay
```

Following drivers are required in the system `PATH` (e.g. `/usr/local/bin`)

* `geckodriver` [download](https://github.com/mozilla/geckodriver/releases)
* `chromedriver` [download](https://sites.google.com/a/chromium.org/chromedriver/downloads)
* `google-chrome-stable` (for ubuntu, in lieu of `chromedriver`)

A valid ClassicalArchives user account is required to automatically download the MIDIs (using `get_composer_midis.py`, see below). The account information should be provided in a json format (by default `data/cma.credential.json`)

```javascript
{
    "username": "aaa",
    "password": "bbb"   
}
```	
	

### Procedures

To get all composers in json format and a list of composer ids. Outputs are `data/composers_[timestamp].json` and `data/composers_[timestamp].list`.

```bash
python3  script/get_all_composers.py 
```


To get all works of all composers in a given list (e.g. `data/composers_[timestamp].list`). Output json files are in the `data/composer` directory (e.g. `data/composer/2113.json`). It skips if outupt json file exists. *For composers with lots of works e.g. Bach (ID=2113), this step may take a couple of hours. However, the site only allows for a single login session.*

```bash
python3  scripts/get_composer_works.py  [composers.list]
```


To check if the number of MIDIs for each composer in an input list (e.g. `data/composers_[timestamp].list`) is consistent within the composer json file (`mode=local`), or is up-to-date with the number of MIDIs online (`mode=online`). *This may take a while with thousands of composers.* 

```bash
python3  script/check_composer_ntrack.py  [composers.list]  [local|online]
```


To generate a download list of all MIDIs (e.g. `data/midis_[timestamp].list`) for all composers in an input list (e.g. `data/composers_[timestamp].list`). The outupt MIDI list is of format `composer_id,work_id,page_id,track_id`. One work may consist of multiple movements (or `track`s) contributed by multiple users (each in one `page`).

```bash
python3  scripts/make_track_list.py  [composers.list]  [midis.list]
```


To view a json file, optionally with key.subkey.subsubkey... with possible list index if the (sub)value is a list.

```bash
python3  script/print_json.py  [input.json]  [key.subkey.subsubkey]
python3  script/print_json.py  [input.json]  [key[index].subkey[index].subsubkey[index]]
```


To download MIDIs provided in an input list (e.g. `data/midis_[timestamp].list`) (existing outputs will be skipped). The output will be saved as `data/midi/[composer_id]/*.mid`. Due to daily download limit (100) set by the website, this script should be used in the cron job.

``` bash
python3  script/get_composer_midis.py  [midis.list]
```


### About remote GUI webdriver display

The scripts uses Selenium `phantomjs` driver mostly (except for `get_composer_midis.py` which uses `chromedriver` for stability concerns). Originally the GUI webdriver would require setting of environment variable `$DISPLAY`, e.g. `export DISPLAY=:0 python3 script.py`. Since `PyVirtualDisplay` is used, no GUI webdriver will pop up and the script can be safely used remotely under ssh. 


## TODO:

* pylint
* argparse
* to scrape http://midiworld.com/bach.htm

