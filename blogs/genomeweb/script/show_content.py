# -*- coding: utf-8 -*-

import os, sys, json, gzip
import re
from lxml import etree

# -------------------------------------------------------------------------

def write_text(text, text_name, verbose=True):

    if verbose:
        qprint('write ' + text_name)
    if text_name.endswith('.gz'):
        fout = gzip.open(text_name, 'wb')
        fout.write((text+'\n').encode('utf-8'))
    else:
        fout = open(text_name, 'w')
        fout.write(text+'\n')
    fout.close()

# -------------------------------------------------------------------------

def read_text(text_name, verbose=True):

    if verbose:
        qprint('read ' + text_name)
    if text_name.endswith('.gz'):
        text = gzip.open(text_name).read().decode('utf-8')
    else:
        text = open(text_name).read()
    return text

# -------------------------------------------------------------------------

def get_timestamp(fmt_str="%Y%m%d%H%M"):

    timestamp = datetime.datetime.now().strftime(fmt_str)
    return timestamp

# -------------------------------------------------------------------------

def qprint(msg, verbose=True):
    print(':: ' + msg, file=sys.stderr, flush=True)

# -------------------------------------------------------------------------

def qopen(fname, mode='r', verbose=True):

    if verbose:
        if mode == 'w':
            qprint('writing {}'.format(fname))
        else:
            qprint('reading {}'.format(fname))

    return open(fname, mode)

# -------------------------------------------------------------------------

def write_json(data, json_name, verbose=True):
    if verbose:
        qprint('write ' + json_name)
    if json_name.endswith('.gz'):
        fout = gzip.open(json_name, 'wb')
        fout.write((json.dumps(data, sort_keys=True) + '\n').encode('utf-8'))
    else:
        fout = open(json_name, 'w')
        fout.write(json.dumps(data, sort_keys=True) + '\n')
    fout.close()

# -------------------------------------------------------------------------

def read_json(json_name, verbose=True):
    if verbose:
        qprint('read ' + json_name)
    if json_name.endswith('.gz'):
        data = json.loads(gzip.open(json_name).read().decode('utf-8'))
    else:
        data = json.loads(open(json_name).read())
    return data


# -------------------------------------------------------------------------

def show_content(in_html_gz):

    text = read_text(in_html_gz, verbose=False)
    root = etree.HTML(text)
    out = {
        'url': 'https://' + re.findall(r'/(www.genomeweb.com/.*?).html.gz', in_html_gz)[0],
        'title': None,
        'date': None,
        'content': [],
        'keyword': {},
        'type_node': None,
        'type_page': None,
        'has_content': True,
    }

    if 'www.genomeweb.com/resources/conferences-events/' in out['url']:
        out['has_content'] = False

    try:
        body_class = root.xpath('//body/@class')[0]
        if 'page-' not in body_class:
            out['has_content'] = False
            raise

        out['type_page'] = [x for x in re.findall(r'page-(.*?) ', body_class) if '-' not in x][0]
        if out['type_page'] in ['taxonomy', 'resources']:
            out['has_content'] = False

        if 'node-type-' in body_class:
            out['type_node'] = re.findall(r'node-type-(.*?) ', body_class)[0]
            if out['type_node'] in ['resource', 'ss-blog', 'ss-bio', 'page', 'job', 'webinar', 'webform']:
                out['has_content'] = False

        out['title'] = root.xpath('//h1[contains(@class, "page-title")]')[0].text
        out['date'] = root.xpath('//span[@class="date-display-single"]')[0].text

        for schema in ['articleBody', 'text']:
            for el in ['p', 'div', 'li', 'pre', 'span']:
                for x in root.xpath('//div[@property="schema:{}"]//{}'.format(schema, el)):
                    txt = re.sub(r'\s+', ' ', ' '.join(x.itertext())).strip()
                    if txt == '':
                        continue
                    out['content'].append(txt)

        for x in root.xpath('//div[contains(@class, "group-filedunder")]//a[@typeof="skos:Concept"]'):
            out['keyword'][x.xpath('./@href')[0]] = x.text

    except Exception as e:
        pass
        # qprint('*ERROR* failed to extract {}'.format(in_html_gz))
        # raise

    return out



def loop(infile_list, outfile_list):

    fout = qopen(outfile_list, 'w')
    for line in qopen(infile_list):
        data = show_content(line.rstrip())
        print(json.dumps(data, sort_keys=True), flush=True, file=fout)
    fout.close()

    pass




if __name__ == '__main__':

    # in_html_gz = sys.argv[1]
    # out = show_content(in_html_gz)
    # print(json.dumps(out, sort_keys=True), flush=True)

    infile_list, outfile_list = sys.argv[1:3]
    loop(infile_list, outfile_list)


# end
