# Get notified for www.thisiscolossal.com

import requests
import json
from bs4 import BeautifulSoup
import re
import os
"""Request"""

REQUEST_HEADERS = {
    'user-agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.5',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded',
    'pragma': 'no-cache',
    'origin': 'https://www.thisiscolossal.com',
    'referer': 'https://www.thisiscolossal.com/'
}


def get_homepage(page: int):
    url = f"https://www.thisiscolossal.com/"
    if page > 1:
        url += f"page/{page}/"
    r = requests.get(url, headers=REQUEST_HEADERS)
    # content = open("thisiscolossal.html").read()
    content = r.content
    soup = BeautifulSoup(content, 'html.parser')
    posts = []
    for item in soup.find_all(id="posts"):
        post = {}
        header = item.find('h2')
        post['title'] = header.getText()
        post['url'] = header.find('a')['href']
        post['date'] = item.find('h3', {'class': 'date'}).getText()
        author = item.find('h3', {'class': 'author'})
        post['author'] = author.getText()
        post['author_url'] = author.find('a')['href']
        text = [p.getText() for p in item.find_all('p', recursive=False)]
        text = '\n'.join(text).strip()
        if len(text) > 1600:
            text = text[:1600 - 3] + '...'
        post['text'] = text
        imgs = item.find_all('img',
                             {'class': re.compile(r"wp-image-\d+ size-full")})
        post['imgs'] = [img['src'] for img in imgs]
        posts.append(post)
    return posts


def generate_embeds(post):
    # generate embed
    embed = {
        'type': "rich",
        'title': post['title'],
        'url': post['url'],
        'author': {
            'name': post['author'],
            'url': post['author_url']
        },
        'description': post['text'],
        'image': {
            'url': post['imgs'][0]
        },
        'footer': {
            'text': post['date']
        }
    }
    embeds = [embed]
    for i in range(1, min(len(post['imgs']), 10)):
        embeds.append({
            'type': "rich",
            'url': post['url'],
            'image': {
                'url': post['imgs'][i]
            },
        })
    return embeds


"""Main"""


def send_message(content, embeds):
    message = {
        "username": "thisiscolossal.com notifier",
        "avatar_url": "https://www.thisiscolossal.com/favicon-32x32.png",
        "content": content,
        'embeds': embeds
    }
    r = requests.post(os.getenv("COLOSSAL_WEBHOOK_URL"),
                      headers={'Content-Type': 'application/json'},
                      data=json.dumps(message))
    assert r.status_code in [200, 204]


FILENAME = ".colossal_checked.json"
try:
    with open(FILENAME, 'r') as fp:
        checked = set(json.load(fp))
except:
    checked = set()
    send_message("thisiscolossal.com checked post list initialized.", [])

posts = sum([get_homepage(page) for page in [3, 2, 1]], [])
for post in posts[::-1]:
    if post['url'] in checked:
        continue
    send_message("", generate_embeds(post))
    # for i in range(0, len(post['imgs'])+4, 5):
    #     imgs = post['imgs'][i:i+5]
    #     send_message('\n'.join(imgs), []);
    checked.add(post['url'])

with open(FILENAME, 'w') as fp:
    json.dump(sorted(checked), fp)

