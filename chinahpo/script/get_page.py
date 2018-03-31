import sys
import requests

input_id, html = sys.argv[1:3]

# header = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
headers = {
    # 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    'Authorization': 'Token 955290c5fbddd689e179fcd63dd4fe39b880b222',
}

if input_id.startswith('HP:'):
    url = 'http://49.4.68.254:8081/knowledge/hpo/{}'.format(input_id)
elif input_id.startswith('OMIM:'):
    input_id = input_id.split(':')[1]
    url = 'http://49.4.68.254:8081/knowledge/omim/{}'.format(input_id)
elif input_id.startswith('ORDO:'):
    input_id = input_id.split(':')[1]
    url = 'http://49.4.68.254:8081/knowledge/orphanet/{}'.format(input_id)
else:
    sys.exit('Unknown ID (must be HP:, OMIM:, ORDO:).')

r = requests.get(url, headers=headers)
fout = open(html, 'w')
print(r.text, file=fout)
fout.close()

# python3 get_page.py "" good2.json
    # url = 'http://49.4.68.254:8081/knowledge/hpo/?search=HP%3A0000726&type=0&page=1'
