import sys
import requests
import json




def get_page(in_cookie_name, in_url, out_html_name):

    cookies = json.loads(open(in_cookie_name).read())

    s = requests.Session()
    for c in cookies:
        s.cookies.set(c['name'], c['value'])

    r = s.get(in_url)
    fout = open(out_html_name, 'w')
    print(r.text, file=fout)
    fout.close()
    for line in r.text.split('\n'):
        if 'schema:articleBody' in line:
            print(line.rstrip())
    print('paywall-box' in r.text)


if __name__ == '__main__':

    # url = 'https://www.genomeweb.com/cancer/nci-pediatric-match-trial-takes-shape-study-expected-open-year?utm_medium=TrendMD&utm_campaign=0&utm_source=TrendMD&trendmd-shared=0#.WxZRjlMvymk'
#     url = 'https://www.genomeweb.com/regulatory-news/european-data-protection-law-brings-new-responsibilities-possibilities-genomics#.WxRsCFMvzYI'
    # url = 'https://www.genomeweb.com/microarrays-multiplexing/migraine-risk-contributions-common-variants-supported-new-studies#.WxhYFmPWFhE'
    # url = 'https://www.genomeweb.com/molecular-diagnostics/cancer-genetics-wins-510k-clearance-tissue-origin-test#.Wxhyc2PWFhE'
    # url = 'https://www.genomeweb.com/microarrays-multiplexing/sporadic-als-risk-appears-overlap-slightly-other-neurodegenerative#.WxhzZmPWFhE'
    url = sys.argv[1]
    out = 'foo.html'
    get_page('cookies2.json', url, out)
