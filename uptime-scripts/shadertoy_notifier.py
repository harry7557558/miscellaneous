# Get notified for Shadertoy highly-liked shaders

import requests
import json
import time
import datetime
import re
import os
"""Request Shaders"""

REQUEST_HEADERS = {
    'user-agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.5',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded',
    'pragma': 'no-cache',
    'origin': 'https://www.shadertoy.com',
    'referer': 'https://www.shadertoy.com/'
}


def get_shaders_page(page: int):
    url = f"https://www.shadertoy.com/results?query=&sort=newest&from={12*page}&num=12"
    r = requests.get(url, headers=REQUEST_HEADERS)
    print("Request", url, "-", r.status_code)
    if r.status_code != 200:
        return []
    lines = [l.strip() for l in r.text.split('\n')] + ['']
    for line in lines:
        if line.startswith('var gShaders='):
            break
    if line == '':
        return []
    line = line.lstrip("var gShaders=")
    line = line[:line.rfind(']') + 1]
    try:
        return json.loads(line)
    except:
        return []


def get_shaders(shader_ids: list):
    print("Request Shadertoy")
    data = {
        's': json.dumps({"shaders": shader_ids}),
        'nt': '1',
        'nl': '1',
        'np': '1'
    }
    req = requests.post("https://www.shadertoy.com/shadertoy",
                        data=data,
                        headers=REQUEST_HEADERS)
    if req.status_code != 200:
        return None
    response = req.content.decode('utf-8')
    response = json.loads(response)
    if len(response) == 0:
        return None
    return response


def get_all_shaders(max_pages: int, max_dt: int, min_likes: int):
    all_shaders = []
    for page in range(max_pages):
        shaders = get_shaders_page(page)
        if len(shaders) < 12:
            break
        for shader in shaders:
            info = shader['info']
            if time.time() - int(info['date']) > max_dt:
                return all_shaders
            if info['likes'] >= min_likes:
                all_shaders.append(shader)
    ids = [shader['info']['id'] for shader in all_shaders]
    return get_shaders(ids)


"""Embed Generation
https://github.com/harry7557558/bot7557558/blob/master/shadertoy.py
"""


def minify_code(code: str):
    """Grabbed from Shadertoy implementation"""

    def isSpace(s):
        return s in [' ', '\t']

    def isLine(s):
        return s == '\n'

    def replaceChars(s):
        dst = ""
        isPreprocessor = False
        for i in range(len(s)):
            if s[i] == "#":
                isPreprocessor = True
            elif s[i] == "\n":
                if isPreprocessor:
                    isPreprocessor = False
                else:
                    dst += " "
                    continue
            elif s[i] in ["\r", "\t"]:
                dst += " "
                continue
            elif i < len(s) - 1 and s[i] == "\\" and s[i + 1] == "\n":
                i += 1
                continue
            dst += s[i]
        return dst

    def removeEmptyLines(s):
        d = ""
        isPreprocessor = False
        for i in range(len(s)):
            if s[i] == '#':
                isPreprocessor = True
            isDestroyableChar = isLine(s[i])
            if isDestroyableChar and not isPreprocessor:
                continue
            if isDestroyableChar and isPreprocessor:
                isPreprocessor = False
            d += s[i]
        return d

    def removeMultiSpaces(s):
        dst = ""
        for i in range(len(s)):
            if isSpace(s[i]) and i == len(s) - 1:
                continue
            if isSpace(s[i]) and isLine(s[i - 1]):
                continue
            if isSpace(s[i]) and isLine(s[i + 1]):
                continue
            if isSpace(s[i]) and isSpace(s[i + 1]):
                continue
            dst += s[i]
        return dst

    def removeSingleSpaces(s):
        dst = ""
        for i in range(len(s)):
            iss = isSpace(s[i])
            if i == 0 and iss:
                continue
            if i > 0:
                if iss and s[i - 1] in ";,}{()+-*/?<>[]:=^%\n\r":
                    continue
            if i > 1:
                if iss and s[i - 2:i] in ["&&", "||", "^^", "!=", "=="]:
                    continue
            if iss and s[i + 1] in ";,}{()+-*/?<>[]:=^%\n\r":
                continue
            if i < len(s) - 2:
                if iss and s[i + 1:i + 3] in ["&&", "||", "^^", "!=", "=="]:
                    continue
            dst += s[i]
        return dst

    def removeComments(s):
        dst = ""
        state = 0
        i = 0
        while i < len(s):
            if i <= len(s) - 2:
                if state == 0 and s[i:i + 2] == "/*":
                    state = 1
                    i += 2
                    continue
                if state == 0 and s[i:i + 2] == "//":
                    state = 2
                    i += 2
                    continue
                if state == 1 and s[i:i + 2] == "*/":
                    dst += " "
                    state = 0
                    i += 2
                    continue
                if state == 2 and s[i] in "\r\n":
                    state = 0
                    i += 1
                    continue
            if state == 0:
                dst += s[i]
            i += 1
        return dst

    code = removeComments(code)
    code = replaceChars(code)
    code = removeMultiSpaces(code)
    code = removeSingleSpaces(code)
    code = removeEmptyLines(code)
    return code


def get_description(info):
    s = info['description']
    # parent
    if 'parentid' in info and info['parentid'] != '':
        prefix = f"Forked from {info['parentname']} (https://www.shadertoy.com/view/{info['parentid']})\n\n"
        s = prefix + s
    # clear formatting
    s = re.sub(r'\[([a-z]+)\](.*?)\[\/\1\]', '\\2', s)
    # hyperlink
    s = re.sub(r'\[url=([\"\']?)(.*?)\1\](.*?)\[\/url\]', '\\3 (\\2)', s)
    return s


def generate_embed(shader: dict):
    info = shader['info']
    shader_id = info['id']
    title = info['name']
    author = info['username']
    date = datetime.datetime.fromtimestamp(int(info['date']))
    description = get_description(info)
    tags = ', '.join(info['tags'])
    views = info['viewed']
    likes = info['likes']
    like_rate = 100.0 * min(float(likes) / max(float(views), 1), 1.0)
    status = {
        0: "private",
        1: "public",
        2: "unlisted",
        3: "public+api"
    }[info['published']]
    footer = " • ".join([tags, status])
    thumb_url = f"https://www.shadertoy.com/media/shaders/{shader_id}.jpg?t={int(time.time())}"
    author_url = f"https://www.shadertoy.com/user/{author}"
    author_icon_url = "https://www.shadertoy.com/img/profile.jpg"
    for ext in ['png', 'jpeg', 'jpg']:
        url = f"https://www.shadertoy.com/media/users/{author}/profile.{ext}"
        r = requests.get(url, headers=REQUEST_HEADERS)
        print("Request", url, "-", r.status_code)
        if r.status_code < 300:
            author_icon_url = url
            break

    # renderpass

    orders = [
        "Common", "Buffer A", "Buffer B", "Buffer C", "Buffer D", "Cube A",
        "Image", "Sound"
    ]
    passes = []

    mains_count = {
        'mainImage': 0,
        'mainSound': 0,
        'mainVR': 0,
    }
    uniforms_count = {
        'iResolution': 0,
        'iTime': 0,
        'iTimeDelta': 0,
        'iChannelTime': 0,
        'iFrame': 0,
        'iMouse': 0,
        'iDate': 0,
        'iSampleRate': 0,
        'iChannelResolution': 0,
    }
    textures_count = {
        'buffer': 0,
        'texture': 0,
        'cubemap': 0,
        'video': 0,
        'music': 0,
        'musicstream': 0,
        'mic': 0,
        'webcam': 0,
        'volume': 0,
        'keyboard': 0,
    }

    for renderpass in shader['renderpass']:
        name = renderpass['name']
        name = name.replace("Buf ", "Buffer ")
        if name == "":
            name = "Image"
        assert name in orders
        code = minify_code(renderpass['code'])
        open(".code.temp", "w").write(minify_code(code))  # check for bug
        passes.append({"name": name, "chars": len(code)})
        words = re.sub(r"[^A-Za-z0-9_]+", ' ', code).strip()
        for word in words.split():
            if word in mains_count:
                mains_count[word] += 1
            if word in uniforms_count:
                uniforms_count[word] += 1
        for input in renderpass['inputs']:
            if input['type'] in textures_count:  # should be
                textures_count[input['type']] += 1

    if len(passes) == 1:
        passes_str = passes[0]['name'] + " • " + \
            str(passes[0]['chars']) + " chars"
    else:
        passes = sorted(passes, key=lambda rp: orders.index(rp['name']))
        passes_name_str = " • ".join([ps['name'] for ps in passes])
        passes_chars = [ps['chars'] for ps in passes]
        passes_chars_str = " + ".join(map(str, passes_chars)) + \
            " = " + str(sum(passes_chars)) + " chars"
        passes_str = passes_name_str + "\n" + passes_chars_str

    mains = [item[0] for item in mains_count.items() if item[1] > 0]
    uniforms = [item[0] for item in uniforms_count.items() if item[1] > 0]
    textures = [item[0] for item in textures_count.items() if item[1] > 0]
    ios = ' ｜ '.join(
        [' • '.join(s) for s in [mains, uniforms, textures] if s != []])
    passes_str += '\n' + ios

    # generate embed
    embed = {
        'type':
        "rich",
        'title':
        title,
        'url':
        "https://www.shadertoy.com/view/" + shader_id,
        'author': {
            'name': author,
            'url': author_url,
            'icon_url': author_icon_url
        },
        'description': description,
        'image': {
            'url': thumb_url
        },
        'footer': {
            'text': footer
        },
        'timestamp':
        str(date),
        'fields': [
            {
                'name': "Renderpass",
                'value': passes_str,
                'inline': False
            },
            {
                'name': "Views",
                'value': str(views),
                'inline': True
            },
            {
                'name': "Likes",
                'value': str(likes),
                'inline': True
            },
            {
                'name': "Like rate",
                'value': "{:.2f} %".format(like_rate),
                'inline': True
            },
        ]
    }
    return embed


"""Main"""


def send_message(content, embeds):
    message = {
        "username": "Shadertoy Notifier",
        "avatar_url":
        "https://www.shadertoy.com/media/users/harry7557558/profile.png",
        "content": content,
        'embeds': embeds
    }
    r = requests.post(os.getenv("SHADERTOY_WEBHOOK_URL"),
                      headers={'Content-Type': 'application/json'},
                      data=json.dumps(message))
    assert r.status_code in [200, 204]


FILENAME = ".shadertoy_checked.json"
try:
    with open(FILENAME, 'r') as fp:
        checked_shaders = set(json.load(fp))
except:
    checked_shaders = set()
    send_message("Checked shader list initialized.", [])

MAX_PAGES = 12
MAX_DT = 86400 * 7
MIN_LIKES = 10
shaders = get_all_shaders(MAX_PAGES, MAX_DT, MIN_LIKES)
for shader in shaders[::-1]:
    if shader['info']['id'] in checked_shaders:
        continue
    dt = time.time() - int(shader['info']['date'])
    time_taken = MIN_LIKES / int(shader['info']['likes']) * (dt / 3600)
    stars = ''.join([":star:" for h in [40, 20, 10, 5, 2] if time_taken < h])
    send_message(
        "Achieved {:d} likes in {:.1f} hours. {}".format(
            MIN_LIKES, time_taken, stars), [generate_embed(shader)])
    checked_shaders.add(shader['info']['id'])

with open(FILENAME, 'w') as fp:
    json.dump(sorted(checked_shaders), fp)
