# Get all messages in a Discord server

import requests
import json
import os


ROOT = "https://discord.com/api/v9"
GUILDS = [
    822212636619309056,  # bot spam
    959874115311906957,  # EngSci 2T6
    1078486370252771369,  # EngSci 2T7
    826076379912994857,  # EngSci 2T5
    1079271713818288179,  # Frosh 2T3
    1076975255475732490,  # Robo 2T5
    1074923999320092714,  # MI 2T5
    1132786163225206904,  # DS101
]
CHANNELS = [
    1038182905228300360,  # CIV102 bridge
    1026554291948896286,  # Praxis I
    1067147631970762813,  # Praxis II
    1131300770160058398,  # UTMIST
]

HEADERS = {
    "authorization": open(".token").read().split()[0],
    "origin": "https://discord.com",
    "referer": "https://discord.com/channels/{GUILD_ID}/",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json",
}


def get_existing_messages():
    all_messages = {}
    for filename in os.listdir():
        if os.path.isfile(filename) and filename.endswith('.json'):
            try:
                with open(filename, 'r') as fp:
                    messages = json.load(fp)
                for message in messages:
                    all_messages[message['id']] = message
                print('Loaded', filename)
            except:
                pass
    print(len(all_messages), 'messages loaded')
    return all_messages

existing_messages = {}


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
        reach_end = False
        for message in parsed:
            if message['id'] in existing_messages:
                reach_end = True
            else:
                existing_messages[message['id']] = message
        if len(parsed) < limit or reach_end:
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
    if len(GUILDS) != 1:
        existing_messages = get_existing_messages()
    for GUILD_ID in GUILDS:
        channels = fetch_channels()
        messages = []
        for channel in channels:
            print(channel['name'])
            fetched = fetch_messages(channel['id'])
            for message in fetched:
                message['channel_name'] = channel['name']
            messages += fetched
        if len(GUILDS) == 1:
            with open("messages.json", "w") as fp:
                json.dump(messages, fp)
    if len(GUILDS) != 1:
        for CHANNEL_ID in CHANNELS:
            print(CHANNEL_ID)
            fetched = fetch_messages(CHANNEL_ID)
        existing_messages = sorted(existing_messages.values(),
                                   key=lambda m: (m['channel_id'], m['timestamp']))
        with open("messages_all.json", "w") as fp:
            json.dump(existing_messages, fp)

