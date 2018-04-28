import sys
import requests

def load_cookies(cookie_name):

    print('loading cookie: {}'.format(cookie_name))
    cookies_str = open(cookie_name).read().strip().replace('\n','')
    cookies_dict = dict()
    for x in cookies_str.split(';'):
        y = x.strip().split('=', 1)
        cookies_dict[y[0]] = y[1]
    return cookies_dict

headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}

url, html = sys.argv[1:3]

if len(sys.argv) == 4:
    cookies_name = sys.argv[3]
    cookies = load_cookies(cookies_name)
    print('get url: {}'.format(url))
    r = requests.get(url, cookies=cookies, headers=headers)
else:
    print('get url: {}'.format(url))
    r = requests.get(url, headers=headers)


print('writing html: ' + html)
fout = open(html, 'w')
print(r.text.replace('\r', '\n'), file=fout)
fout.close()
