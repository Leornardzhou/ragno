### Usage:

Create a list of receipt numbers to query (e.g. `rcpt.list`) with one number per line (e.g. `SRC1890055000`), 
then run the following script,

```bash
python3 scripts/scripts/query_my_cases.py  [rcpt.list]
```

The output status report will be saved in  `data/[YYYYMMDD].status.log`. The report format is, 

```
receipt_number1    {'title': xxxx, 'message': xxx}
receipt_number2    {'title': xxxx, 'message': xxx}
receipt_number3    {'title': xxxx, 'message': xxx}
```





