# Get the most frequently used emojis
# Default: message contents + reactions, past 6 months, 20 emojis

import json
import re
import codecs
from datetime import datetime


def load_emoji_list():
    """Get a list of emojis"""
    result = []

    # load a list of emojis
    with open("emojis.json", "r") as fp:
        shortcut_unicode = json.load(fp)

    def recurse(emojis: list):
        nonlocal result
        for emoji in emojis:
            assert "names" in emoji
            assert "surrogates" in emoji
            surrogates = emoji['surrogates']
            for name in emoji['names']:
                if re.match("u[A-Za-z0-9]{4}", name):
                    continue
                result.append({
                    'name': name,
                    'unicode': surrogates
                })
            if "diversityChildren" in emoji:
                recurse(emoji['diversityChildren'])

    for (category, emojis) in shortcut_unicode.items():
        if category in ['flags']:
            continue
        assert type(emojis) is list
        recurse(emojis)

    result.sort(key=lambda x: -len(x['unicode']))
    return result


def stat_emojis(messages, emojis):

    # get all messages as a single string
    contents = []
    for message in messages:
        # past 6 months
        timestamp = datetime.fromisoformat(message['timestamp'])
        timestamp = timestamp.replace(tzinfo=None)
        dt = datetime.now() - timestamp
        #if dt.days >= 180:
        #    continue
        # reactions
        content = ''
        if 'reactions' in message:
            for reaction in message['reactions']:
                emoji = reaction['emoji']
                if emoji['id'] is None:
                    emoji = emoji['name']
                else:
                    continue
                    emoji = f"<:{emoji['name']}:{emoji['id']}>"
                content += emoji * reaction['count'] + '\n'
        # content
        content = message['content'] + '\n' + content
        if True:
            content = ''.join(set(list(content)))
        contents.append(content)
    open('.txt', 'w').write('\n'.join(contents))
    contents = '\n'.join(contents)

    counts = {}
    # default emojis
    for emoji in emojis:
        emoji, unicode = ':'+emoji['name']+':', emoji['unicode']
        #count = contents.count(emoji)
        count = contents.count(unicode)
        if count != 0:
            if unicode not in counts:
                counts[unicode] = 0
            counts[unicode] += count
            contents = contents.replace(unicode, '')  # hmmm...
    # custom emojis
    #for match in re.findall(r"<\:[^\:\<\>]+\:\d+>", contents):
    #    if match not in counts:
    #        counts[match] = 0
    #    counts[match] += 1

    # tops
    counts = list(counts.items())
    counts.sort(key=lambda x: -x[1])
    with open("emoji_counts.json", "w") as fp:
        json.dump(counts, fp, ensure_ascii=False)
    for count in counts[:20]:
        print('\t'.join(map(str, count)))


if __name__ == "__main__":

    emojis = load_emoji_list()

    with open("messages_all.json", "r") as fp:
        messages = json.load(fp)

    stat_emojis(messages, emojis)
