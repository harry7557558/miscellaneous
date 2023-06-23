# Get all messages in a Discord server

import requests
import json


ROOT = "https://discord.com/api/v9"
# GUILD_ID = 822212636619309056  # bot spam
# GUILD_ID = 959874115311906957  # EngSci 2T6
# GUILD_ID = 1078486370252771369  # EngSci 2T7
# GUILD_ID = 826076379912994857  # EngSci 2T5
GUILD_ID = 1079271713818288179  # Frosh 2T3

HEADERS = {
    "authorization": open(".token").read().strip(),
    "origin": "https://discord.com",
    "referer": "https://discord.com/channels/{GUILD_ID}/",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json",
}


def fetch_messages(channel_id):
    limit = 100
    before = None
    messages = []
    while True:
        qs = f"limit={limit}"
        if before is not None:
            qs += f"&before={before}"
        url = f"{ROOT}/channels/{channel_id}/messages?{qs}"
        print(url)
        r = requests.get(url, headers=HEADERS)
        if r.status_code != 200:
            print(r.status_code)
            break
        parsed = json.loads(r.text)
        messages += parsed
        if len(parsed) < limit:
            break
        before = parsed[-1]['id']
    return messages


def fetch_channels():
    url = f"{ROOT}/guilds/{GUILD_ID}/channels"
    r = requests.get(url, headers=HEADERS)
    if r.status_code != 200:
        print(r.status_code)
        return []
    channels = json.loads(r.text)
    filtered = []
    for channel in channels:
        if channel['type'] == 0:
            filtered.append(channel)
    return filtered


if __name__ == "__main__":

    channels = fetch_channels()
    messages = []
    for channel in channels:
        print(channel['name'])
        fetched = fetch_messages(channel['id'])
        for message in fetched:
            message['channel_name'] = channel['name']
        messages += fetched
    with open("messages.json", "w") as fp:
        json.dump(messages, fp)
