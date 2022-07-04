# Send messages with my stuff as PFP and see which ones look nice

import json
import requests
from bs4 import BeautifulSoup
import time


with open(".webhooks", 'r') as fp:
    webhooks = json.load(fp)
    webhook_url = webhooks['pfpBot']


def send_pfp(content, avatar_url):
    contents = {
        'content': content,
        'username': str(int(time.time())),
        'avatar_url': avatar_url
    }
    r = requests.post(
        webhook_url,
        data=contents
    )
    print(avatar_url, '-', r.status_code)
    time.sleep(2)


def send_desmos():
    url = "https://harry7557558.github.io/desmos/index.html"
    req = requests.get(url)
    print(req.status_code)
    soup = BeautifulSoup(req.content, 'html.parser')
    graphs = soup.find_all('div', {'class': "graph"})
    for graph in graphs:
        name = graph.find('h2').text
        img = graph.find('img').attrs['src']
        send_pfp(name, img)


def send_shadertoy():
    url = "https://harry7557558.github.io/shadertoy/index.html"
    req = requests.get(url)
    print(req.status_code)
    soup = BeautifulSoup(req.content, 'html.parser')
    shaders = soup.find_all('div', {'class': "shader"})
    for shader in shaders:
        name = shader.find('h2').text
        img = shader.find('img', {'loading': "lazy"})['src']
        send_pfp(name, img)


def send_seashells():
    urls = [
        "https://media.discordapp.net/attachments/987164635872526407/993274736664653954/unknown.png",
        "https://media.discordapp.net/attachments/987164635872526407/993275158729081053/unknown.png",
        "https://media.discordapp.net/attachments/987164635872526407/993275444059185192/unknown.png",
        "https://media.discordapp.net/attachments/987164635872526407/993319341393203230/unknown.png",
        "https://media.discordapp.net/attachments/987164635872526407/993319522398380143/unknown.png",
        "https://media.discordapp.net/attachments/987164635872526407/993319701662941255/unknown.png"
    ]
    for i in range(len(urls)):
        name = ' '.join(['Conch', str(i)])
        img = urls[i]
        send_pfp(name, img)


if __name__ == "__main__":
    #send_desmos()
    #send_shadertoy()
    send_seashells()
