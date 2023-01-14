# Statistics on a user's message readability.

import json

import sys
import os
DIR = os.path.abspath(__file__)
DIR = '/'.join(DIR.replace('\\', '/').split('/')[:-3])
sys.path.append(DIR + '/bot7557558')
from word_count import flesch_kincaid_readability as readability

with open(".messages.json", "r") as fp:
    MESSAGES = json.load(fp)


def filter_messages(user):
    msgs = []
    for msg in MESSAGES:
        author = '#'.join([
            msg['author']['username'],
            msg['author']['discriminator']
        ])
        if author == user:
            msgs.append(msg)
    msgs.sort(key=lambda m: m['timestamp'])
    msgs = [m['content'] for m in msgs]
    print(len(msgs), "messages from", user)
    return msgs


def stat_message_readability(msgs):
    nm = len(msgs)
    msgs = '\n'.join(msgs)
    r = readability(msgs)
    if r is None:
        r = (0, 0, 0, "Grade -100", "Sus")
    ns, nw, nuw, grade, ease = r
    grade = int(grade.split()[1])
    return (nm, ns, nw, grade, ease)


def get_all_users():
    users = set()
    for msg in MESSAGES:
        author = msg['author']
        if 'bot' in author and author['bot']:
            continue
        if author['discriminator'] == '0000':
            continue
        author = '#'.join([
            author['username'],
            author['discriminator']
        ])
        users.add(author)
    return users


def get_most_readable_users():
    res = []
    for user in get_all_users():
        msgs = filter_messages(user)
        nm, ns, nw, grade, ease = stat_message_readability(msgs)
        if ns >= 20:
            res.append((user, nm, ns, grade, ease))
    res.sort(key=lambda x: (x[-2], x[-1], x[0]), reverse=True)
    for r in res:
        print(r[0], f"Grade {r[-2]}", r[-1], sep=',  ')
    


#filter_messages("AG2048#0001")
get_most_readable_users()
