# Get all messages in a Discord server

import requests
import json
import os
import datetime
import time


ROOT = "https://discord.com/api/v9"
GUILDS = [
    822212636619309056,  # bot spam
    1188335600126918736,  # spirulae
    826076379912994857,  # EngSci 2T5
    959874115311906957,  # EngSci 2T6
    1078486370252771369,  # EngSci 2T7
    1205550774277636159,  # EngSci 2T8
    1237587525829394432,  # Frosh 2T4
    1079271713818288179,  # Frosh 2T3
    984959608420442132,  # Frosh 2T2
    1132786163225206904,  # DS101
    1188346884264316928,  # EngSci 2T6 Robo
    1211069529589948428,  # EngSci 2T6 MI
    1193723260089675786,  # EngSci 2T6 Aero
    1199461922366562305,  # EngSci 2T6 BME
    1206059028082593902,  # EngSci 2T6 ECE
    1211434529236062269,  # EngSci 2T6 Physics
    1206048310209683486,  # EngSci 2T6 MSF
    1212632317948989510,  # EngSci 2T6 Energy
    1074923999320092714,  # EngSci 2T5 MI
    1076832945794453564,  # EngSci 2T5 ECE
]
CHANNELS = [
    
]

# number of recent days, -1 for unlimited
THREAD_HISTORY = 60

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
checked_threads = set()


def fetch_messages(channel, force_refresh=False):
    print(channel['name'], end=' ')

    if 'last_message_id' in channel and \
        channel['last_message_id'] is not None and \
        channel['last_message_id'] in existing_messages and \
            not force_refresh:
        print("skipped")
        return []

    channel_id = channel['id']
    limit = 100
    before = None
    messages = []
    while True:
        qs = f"limit={limit}"
        if before is not None:
            qs += f"&before={before}"
        url = f"{ROOT}/channels/{channel_id}/messages?{qs}"
        #print(url)
        r = requests.get(url, headers=HEADERS)
        if r.status_code != 200:
            print(r.status_code, end='')
            break
        parsed = json.loads(r.text)
        reach_end = False
        for message in parsed:
            if force_refresh:
                messages.append(message)
            if message['id'] in existing_messages:
                reach_end = True
                break
            else:
                existing_messages[message['id']] = message
                if not force_refresh:
                    messages.append(message)
        if len(parsed) < limit or reach_end:
            break
        before = parsed[-1]['id']
        print('*', end='')
    n_messages = len(messages) - int(force_refresh)
    if n_messages > 0:
        print(f' +{n_messages}', end='')
    print()
    return messages


def fetch_messages_thread(thread):
    global checked_threads
    if thread['id'] in checked_threads:
        return []
    checked_threads.add(thread['id'])

    time = snowflake_time(thread['id'])
    if 'last_message_id' in thread and thread['last_message_id'] is not None:
        time = snowflake_time(thread['last_message_id'])
    now = datetime.datetime.now()
    dt = (now-time).total_seconds()/86400
    if THREAD_HISTORY > 0 and dt > THREAD_HISTORY:
        return []
    fetched = fetch_messages(thread, True)
    for message in fetched:
        message['channel_name'] = thread['name']
    return fetched


def fetch_threads(channel):
    channel_id = channel['id']
    threads = []
    while True:
        url = f"{ROOT}/channels/{channel_id}/threads/archived/public"
        r = requests.get(url, headers=HEADERS)
        time.sleep(0.1)
        if r.status_code != 200:
            if r.status_code != 403:
                print(r.status_code, end='')
            break
        parsed = json.loads(r.text)
        threads += parsed['threads']
        if not parsed['has_more'] or True:
            break
    return threads


def fetch_channels(guild_id):
    url = f"{ROOT}/guilds/{guild_id}/channels"
    r = requests.get(url, headers=HEADERS)
    if r.status_code != 200:
        print(r.status_code)
        return []
    channels = json.loads(r.text)
    filtered = []
    for channel in channels:
        if channel['type'] in [0, 5, 15, 16]:
            filtered.append(channel)
    # return filtered
    return channels


def snowflake_time(snowflake):
    return datetime.datetime.utcfromtimestamp(((int(snowflake) >> 22) + 1420070400000) / 1000)


def main():
    global existing_messages

    if len(GUILDS)+len(CHANNELS) != 1:
        existing_messages = get_existing_messages()

    # guilds
    for GUILD_ID in GUILDS:
        channels = fetch_channels(GUILD_ID)
        messages = []
        all_threads = []
        for channel in channels:
            if channel['type'] in [0, 5]:
                fetched = fetch_messages(channel)
                for message in fetched:
                    message['channel_name'] = channel['name']
                messages += fetched
                if fetched != []:
                    threads = fetch_threads(channel)
                    all_threads += threads
            if channel['type'] in [15, 16]:
                threads = fetch_threads(channel)
                all_threads += threads

        for thread in all_threads:
            fetch_messages_thread(thread)

        if len(GUILDS)+len(CHANNELS) == 1:
            with open("messages.json", "w") as fp:
                json.dump(messages, fp)

    # threads
    for mid in list(existing_messages.keys()):
        message = existing_messages[mid]
        if 'thread' in message:
            messages = fetch_messages_thread(message['thread'])
            last_message_id = message['thread']['last_message_id']
            if last_message_id is None:
                last_message_id = '0'
            for msg in messages:
                if int(msg['id']) > int(last_message_id):
                    last_message_id = msg['id']
            if last_message_id != '0':
                message['thread']['last_message_id'] = last_message_id

    # channels
    if len(GUILDS)+len(CHANNELS) != 1:
        for CHANNEL_ID in CHANNELS:
            CHANNEL_ID = str(CHANNEL_ID)
            fetched = fetch_messages({ 'name': CHANNEL_ID, 'id': CHANNEL_ID })
        existing_messages = sorted(existing_messages.values(),
                                   key=lambda m: (m['channel_id'], m['timestamp']))
        with open("messages_all.json", "w") as fp:
            json.dump(existing_messages, fp)


if __name__ == "__main__":
    main()
