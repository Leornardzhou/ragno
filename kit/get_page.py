import sys
import requests

url, html = sys.argv[1:3]

r = requests.get(url)
fout = open(html, 'w')
print(r.text, file=fout)
fout.close()
