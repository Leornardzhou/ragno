import os
import sys
import json
from kit import utils


def qcmd(cmd):
    print(':: ' + cmd, flush=True, file=sys.stderr)
    retcode = os.system(cmd)
    if retcode:
        raise Exception('*ERROR* non-zero return code ({})!'.format(retcode))


def fix_book48_chapter9(timestamp):

    content_err_list = [
        {
            'vers': '43',
            'text': ('倘若你的手使你跌倒，砍掉它！你残废进入生命，'
                     '比有两只手而往地狱里，到那不灭的火里去更好。'),
        },
        {
            'vers': '45',
            'text': ('＊倘若你的脚使你跌倒，砍掉它！你瘸腿进入生命，'
                     '比有双脚被投入地狱里更好。＊'),
        },
        {
            'vers': '47',
            'text': ('＊倘若你的眼使你跌倒，剜出它来！你一只眼进入天主的国，'
                     '比有两只眼被投入地狱里更好，'),
        },
    ]
    content_fix_list = [
        [
            {
                'vers': '43',
                'text': '倘若你的手使你跌倒，砍掉它！',
            },
            {
                'vers': '44',
                'text': '你残废进入生命，比有两只手而往地狱里，到那不灭的火里去更好。',
            },
        ],
        [
            {
                'vers': '45',
                'text': '倘若你的脚使你跌倒，砍掉它！',
            },
            {
                'vers': '46',
                'text': '你瘸腿进入生命，比有双脚被投入地狱里更好。',
            },
        ],
        [
            {
                'vers': '47',
                'text': '倘若你的眼使你跌倒，剜出它来！你一只眼进入天主的国，比有两只眼被投入地狱里更好，',
            },
        ],
    ]
    fix_it(timestamp, 'book48.chapter9', content_err_list, content_fix_list)


def fix_book48_chapter11(timestamp):

    content_err_list = [
        {
            'vers': '25',
            'text': ('当你们立着祈祷时，若你们有什么怨人的事，就宽恕罢！'
                     '好叫你们在天之父，也宽恕你们的过犯。”＊'),
        },
    ]
    content_fix_list = [
        [
            {
                'vers': '25',
                'text': '当你们立着祈祷时，若你们有什么怨人的事，就宽恕罢！'
            },
            {
                'vers': '26',
                'text': '好叫你们在天之父，也宽恕你们的过犯。”'
            },
        ],
    ]
    fix_it(timestamp, 'book48.chapter11', content_err_list, content_fix_list)


def fix_book49_chapter17(timestamp):

    content_err_list = [
        {
            "vers": "35",
            "text": "两个女人一起推磨，一个要被提去，而一个要被遗弃。”＊",
        },
    ]
    content_fix_list = [
        [
            {
                "vers": "35",
                "text": "两个女人一起推磨，一个要被提去，而一个要被遗弃。”",
            },
        ],
    ]
    fix_it(timestamp, 'book49.chapter17', content_err_list, content_fix_list)


def fix_book51_chapter28(timestamp):

    content_err_list = [
        {
            "text": "所以，你们要知道：天主的这个救恩已送给了外邦人，他们将要听从。”*",
            "vers": "28"
        },
    ]
    content_fix_list = [
        [
            {
                "text": "所以，你们要知道：",
                "vers": "28"
            },
            {
                "text": "天主的这个救恩已送给了外邦人，他们将要听从。”",
                "vers": "29"
            },
        ],
    ]
    fix_it(timestamp, 'book51.chapter28', content_err_list, content_fix_list)



def fix_it(timestamp, book_chapter, content_err_list, content_fix_list):

    fix_dir = '../data/{}.fix'.format(timestamp)
    os.makedirs(fix_dir, exist_ok=True)
    fin_json = '../data/{}/{}.json'.format(timestamp, book_chapter)
    fold_json = '{}/{}.old.json'.format(fix_dir, book_chapter)
    fnew_json = '{}/{}.new.json'.format(fix_dir, book_chapter)

    data = utils.load_json(fin_json)
    new_content = []
    content_changed = False
    for i,x in enumerate(data['content']):
        has_issue = False
        for y,zz in zip(content_err_list, content_fix_list):
            if (x['vers'] == y['vers'] and x['text'] == y['text']):
                has_issue = True
                for z in zz:
                    new_content.append(z)
                content_changed = True
        if not has_issue:
            new_content.append(x)

    if not content_changed:
        print(':: target problem is not found in {}'.format(fin_json),
              file=sys.stderr, flush=True)
        return

    qcmd('cp {} {}'.format(fin_json, fold_json))
    data['content'] = new_content
    utils.write_json(data, fnew_json)
    qcmd('cp {} {}'.format(fnew_json, fin_json))





def fix(timestamp):

    fix_book48_chapter9(timestamp)
    fix_book48_chapter11(timestamp)
    fix_book49_chapter17(timestamp)
    fix_book51_chapter28(timestamp)


if __name__ == '__main__':

    timestamp = sys.argv[1]
    fix(timestamp)
