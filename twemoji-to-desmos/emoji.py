# Scrape emojis from Discord and load them

import json
import os
import requests
import math


def gilbert2d(x: int, y: int, ax: int, ay: int, bx: int, by: int, points: list):
    """
    Generalized Hilbert ('gilbert') space-filling curve for arbitrary-sized
    2D rectangular grids.
    """
    # https://stackoverflow.com/a/58603668
    def sgn(x):
        return 1 if x > 0 else -1 if x < 0 else 0
    (dax, day) = (sgn(ax), sgn(ay))  # unit major direction
    (dbx, dby) = (sgn(bx), sgn(by))  # unit orthogonal direction
    w = abs(ax + ay)
    h = abs(bx + by)
    if h == 1:  # trivial row fill
        for i in range(0, w):
            points.append((x, y))
            (x, y) = (x + dax, y + day)
        return
    if w == 1:  # trivial column fill
        for i in range(0, h):
            points.append((x, y))
            (x, y) = (x + dbx, y + dby)
        return
    (ax2, ay2) = (ax//2, ay//2)
    (bx2, by2) = (bx//2, by//2)
    w2 = abs(ax2 + ay2)
    h2 = abs(bx2 + by2)
    if 2*w > 3*h:
        if (w2 % 2) and (w > 2):  # prefer even steps
            (ax2, ay2) = (ax2 + dax, ay2 + day)
        # long case: split in two parts only
        gilbert2d(x, y, ax2, ay2, bx, by, points)
        gilbert2d(x+ax2, y+ay2, ax-ax2, ay-ay2, bx, by, points)
    else:
        if (h2 % 2) and (h > 2):  # prefer even steps
            (bx2, by2) = (bx2 + dbx, by2 + dby)
        # standard case: one step up, one long horizontal, one step down
        gilbert2d(x, y, bx2, by2, ax2, ay2, points)
        gilbert2d(x+bx2, y+by2, ax, ay, bx-bx2, by-by2, points)
        gilbert2d(x+(ax-dax)+(bx2-dbx), y+(ay-day)+(by2-dby),
                  -bx2, -by2, -(ax-ax2), -(ay-ay2), points)


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


def generate_emoji_table(save_path: str, include_diversity: bool, categories: list[str], slice=slice(None)):
    """Generate a table of emojis"""
    WIDTH = 36  # width of each emoji
    CELLWIDTH = 40  # width of grid cell
    PADDING = (CELLWIDTH-WIDTH)//2  # padding

    SVG_START = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 36 36">'
    SVG_END = '</svg>'

    emojis = get_emoji_list(include_diversity, categories)[slice]
    filenames = [emoji['path'] for emoji in emojis]
    gridsize = int(0.5+len(filenames)**0.5)

    width = gridsize
    height = ((len(filenames)+gridsize-1)//gridsize)
    coords = []
    if width >= height:
        gilbert2d(0, 0, width, 0, 0, height, coords)
    else:
        gilbert2d(0, 0, 0, height, width, 0, coords)
    width, height = width*CELLWIDTH, height*CELLWIDTH

    content = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}">'
    for k in range(len(filenames)):
        # x, y = k % gridsize, k // gridsize
        x, y = coords[k]
        dx = x * CELLWIDTH + PADDING
        dy = y * CELLWIDTH + PADDING
        svg = open("svg/"+filenames[k], 'r').read()
        assert svg.startswith(SVG_START)
        assert svg.endswith(SVG_END)
        content += f"<g transform='translate({dx},{dy})'>"
        content += svg[len(SVG_START):len(svg)-len(SVG_END)]
        content += "</g>"
    content += "</svg>"

    content = bytearray(content, 'utf-8')
    print(f"Merged SVG {len(content)} bytes")
    open(save_path, "wb").write(content)


if __name__ == "__main__":
    # download_emojis()

    generate_emoji_table("info/full.svg", False, None)
    # generate_emoji_table("info/full.svg", False, ['people'], slice(36))
