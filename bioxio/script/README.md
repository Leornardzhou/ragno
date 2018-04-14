Usage:
```bash
python3  scrape.py   <timestamp>
python3  format_csv.py   <timestamp>
```

Ranking example:
```bash
cat ../data/<timestamp>.csv | grep -e ^biology -e ^medicine | sort -t\, -rgk4,4 | more
```
