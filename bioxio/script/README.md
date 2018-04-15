Usage:
```bash
python3  scrape.py   <timestamp>
python3  format_csv.py   <timestamp>
```

Ranking example:
```bash
cat ../data/<timestamp>.csv | grep -e ^biology -e ^medicine | sort -t\, -rgk4,4 | more
```

Note:
Because some journals are not visible under subject lists, for each visible journal, the program further crawls all adjacent journals to collect all existing journals.

