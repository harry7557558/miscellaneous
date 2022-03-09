import json


def get_emoji_list():
    result = []
    with open("discord-emoji-list.json", "r") as fp:
        emoji_json = json.load(fp)

    def recurse(emojis: list):
        nonlocal result
        for emoji in emojis:
            assert "names" in emoji
            assert "surrogates" in emoji
            for name in emoji['names']:
                result.append((name, emoji['surrogates']))
                break  # comment to be spammed
            if "diversityChildren" in emoji:
                continue  # comment
                recurse(emoji['diversityChildren'])

    for emojis in emoji_json.values():
        if type(emojis) != list:
            continue
        recurse(emojis)
    return result


result = get_emoji_list()

print(len(result))
