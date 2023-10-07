import requests
import os
import json
import hashlib


def get_attachments(filename):
    with open(filename, 'r') as fp:
        messages = json.load(fp)

    res = []
    content_types = set({})
    for message in messages:
        if message['author']['id'] not in ['489540173999112230', '946906238808117301']:
            continue
        if 'attachments' not in message:
            continue
        attachments = message['attachments']
        if len(attachments) == 0:
            continue
        for attachment in attachments:
            if 'content_type' not in attachment:
                continue
            content_type = attachment['content_type']
            content_types.add(content_type[:(content_type+';').find(';')])
            #if content_type.startswith('text'):
            #    continue
            url = attachment['url']
            url = url[:(url+'?').find('?')]
            filename = attachment['filename']
            if len(filename) >= 232:
                ext = filename[filename.rfind('.'):]
                hashed = hashlib.md5(bytearray(filename, 'utf-8')).hexdigest()
                filename = hashed + ext
            areas = [
                #message['channel_id'],
                attachment['id'],
                filename
            ]
            res.append((url, '-'.join(areas)))

    print(len(res), "attachments")
    print(content_types)
    return res


def download_attachments(attachments):
    attachments = sorted(set(attachments))
    n = len(attachments)
    print("Total", n, "attachments")
    to_download = []
    for i in range(n):
        url, filename = attachments[i]
        filename = 'attachments/' + filename
        if os.path.isfile(filename):
            continue
        to_download.append((url, filename))
    n = len(to_download)
    print("Download", n, "attachments")
    for i in range(n):
        url, filename = to_download[i]
        r = requests.get(url)
        print(f"{i+1}/{n}", r.status_code, url)
        with open(filename, 'wb') as f:
            f.write(r.content)


def get_all_attachments():
    res = []
    for filename in os.listdir():
        if os.path.isfile(filename):
            if filename.endswith('.json'):
                print(filename)
                try:
                    res += get_attachments(filename)
                except BaseException as e:
                    print("Error:", e)
    print()
    return res


attachments = get_all_attachments()
download_attachments(attachments)
