# Get all roles and channels in a Discord server

import requests
import json


ROOT = "https://discord.com/api/v9"
GUILD_ID = 826076379912994857  # the server to get roles/channels
CHANNEL_ID = 959874115311906962  # the channel to send the message to


HEADERS = {
    "authorization": open(".token").read().strip(),
    "origin": "https://discord.com",
    "referer": "https://discord.com/channels/{GUILD_ID}/",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json",
}


def get_roles(mentionable_only=False):
    url = f"{ROOT}/guilds/{GUILD_ID}"
    r = requests.get(url, headers=HEADERS)
    if r.status_code != 200:
        print(r.status_code)
        return []
    guild = json.loads(r.content)
    roles = guild['roles'][1:]
    roles.sort(key=lambda x: int(x['id']))
    mentions = []
    for role in roles:
        if mentionable_only and not role['mentionable']:
            continue
        name = role['name']
        rid = role['id']
        print(f"<@&{rid}>", "@"+name)
        mentions.append(f"<@&{rid}>")
    return ' '.join(mentions)


def get_channels():
    url = f"{ROOT}/guilds/{GUILD_ID}/channels"
    r = requests.get(url, headers=HEADERS)
    if r.status_code != 200:
        print(r.status_code)
        return []
    channels = json.loads(r.content)
    channels.sort(key=lambda x: int(x['id']))
    mentions = []
    for channel in channels:
        if channel['type'] == 4:
            continue
        name = channel['name']
        topic = channel['topic'] if 'topic' in channel else None
        cid = channel['id']
        print(f"<#{cid}>", '#'+channel['name'],
              '- '+topic if topic is not None else '')
        mentions.append(f"<#{cid}>")
    return ' '.join(mentions)


def send_without_ping(info, content):
    content = content.split(' ')
    temp = info+'\n'
    for i in range(len(content)+1):
        if len(temp) > 1800 or i == len(content):
            message = {
                "content": temp,
                "allowed_mentions": {
                    "parse": []
                }
            }
            url = ROOT + f"/channels/{CHANNEL_ID}/messages"
            r = requests.post(url, headers=HEADERS, data=json.dumps(message))
            print(r.status_code)
            temp = ""
        if i >= len(content):
            break
        temp += content[i] + ' '


if __name__ == "__main__":

    roles = get_roles(False)
    #send_without_ping("All roles.", roles)

    #channels = get_channels()
    #send_without_ping("All channels.", channels)
