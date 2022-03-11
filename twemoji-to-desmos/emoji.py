# Scrape emojis from Discord and load them

import json
import os
import requests


def surrogates_to_unicode(unicode: str) -> str:
    """
    >>> surrogates_to_unicode("😀")
    "./1f600.svg"
    >>> surrogates_to_unicode("👨‍👩‍👧‍👦")
    "./1f468-200d-1f469-200d-1f467-200d-1f466.svg"
    >>> surrogates_to_unicode("©️")
    "./a9-fe0f.svg"
    """
    # unicode = unicode.rstrip('\ufe0f').rstrip('\ufe0e')
    splitted = [hex(ord(c)).lstrip('0x') for c in unicode]
    path = '-'.join(splitted)
    return "./" + path + ".svg"


def get_emoji_list(include_diversity: bool, categories: list[str] = None):
    """Get a list of emojis
    Args:
        include_diversity: whether include diversities of emojis
        categories: a list of strings people|nature|food|activity|travel|objects|symbols|flags
    """
    result = []

    # load a list of emojis
    with open("info/shortcut-unicode.json", "r") as fp:
        shortcut_unicode = json.load(fp)

    def recurse(emojis: list):
        nonlocal result
        for emoji in emojis:
            assert "names" in emoji
            assert "surrogates" in emoji
            surrogates = emoji['surrogates']
            for name in emoji['names']:
                result.append({
                    'name': name,
                    'surrogates': surrogates,
                    'unicode': surrogates_to_unicode(surrogates)
                })
                break  # comment to be spammed
            if include_diversity and "diversityChildren" in emoji:
                recurse(emoji['diversityChildren'])

    for (category, emojis) in shortcut_unicode.items():
        assert type(emojis) is list
        if categories != None and category not in categories:
            continue
        recurse(emojis)

    # get corresponding image
    with open("info/unicode-id.json", "r") as fp:
        unicode_id = json.load(fp)
    with open("info/id-path.json", "r") as fp:
        id_path = json.load(fp)
    for emoji in result:
        if emoji['unicode'] not in unicode_id:  # why?
            emoji['unicode'] = emoji['unicode'].replace('-fe0f', '')
        assert emoji['unicode'] in unicode_id
        emoji['id'] = unicode_id[emoji['unicode']]
        assert emoji['id'] in id_path
        emoji['path'] = id_path[emoji['id']]

    return result


def download_emojis():
    """Scrape all emojis from Discord"""
    emojis = get_emoji_list(True)
    filenames = [emoji['path'] for emoji in emojis]
    for filename in filenames:
        url = "https://discord.com/assets/" + filename
        path = "svg/" + filename
        if os.path.isfile(path):
            # print("Already exists", path)
            continue
        req = requests.get(url)
        if req.status_code != 200:
            print("Error", req.status_code, url)
        else:
            content = req.content
            with open(path, "wb") as fp:
                fp.write(content)


def generate_emoji_table(save_path: str, include_diversity: bool, categories: list[str], max_count: int):
    """Generate a table of emojis"""
    WIDTH = 36  # width of each emoji
    CELLWIDTH = 40  # width of grid cell
    PADDING = (CELLWIDTH-WIDTH)//2  # padding

    SVG_START = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 36 36">'
    SVG_END = '</svg>'

    emojis = get_emoji_list(include_diversity, categories)[:max_count]
    filenames = [emoji['path'] for emoji in emojis]
    gridsize = int(0.5+len(filenames)**0.5)

    width = CELLWIDTH * gridsize
    height = CELLWIDTH * ((len(filenames)+gridsize-1)//gridsize)
    content = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}">'
    for k in range(len(filenames)):
        x, y = k % gridsize, k // gridsize
        dx = x * CELLWIDTH + PADDING
        dy = y * CELLWIDTH + PADDING
        svg = open("svg/"+filenames[k], 'r').read()
        assert svg.startswith(SVG_START)
        assert svg.endswith(SVG_END)
        content += f"<g transform='translate({dx},{dy})'>"
        content += svg[len(SVG_START):len(svg)-len(SVG_END)]
        content += "</g>"
    content += "</svg>"

    open(save_path, "w").write(content)


if __name__ == "__main__":
    # download_emojis()
    generate_emoji_table("info/full.svg", False, ['nature'], 16)
