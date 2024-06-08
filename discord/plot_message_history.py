# Generate and plot message statistics
# Run `fetch_messages.py` to generate `.messages.json`

import json
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy.ndimage import gaussian_filter


MESSAGES = []

def load_messages(guild_id=None):
    global MESSAGES

    if guild_id is None:
        with open("messages_all.json", "r") as fp:
            MESSAGES = json.load(fp)
    else:
        from fetch_messages import fetch_channels
        channels = set()
        if type(guild_id) is not list:
            guild_id = [guild_id]
        for gi in guild_id:
            for channel in fetch_channels(gi):
                channels.add(channel['id'])
        with open("messages_all.json", "r") as fp:
            messages = json.load(fp)
        for message in messages:
            if message['channel_id'] in channels:
                MESSAGES.append(message)
    MESSAGES.sort(key=lambda m: int(m['id']))


IGNORE_DELETED = False
NUM_DAYS = 180
NUM_TOPS = 20
AUTHORS = {}
CHANNELS = {}


def generate_date_attr(attr: str, counter: str):
    """Generate a graph of attribute vs. date
        Attribute is the dictionary key, can be 'author' or 'channel_name'
        Returns a table where the rows are dictionaries and columns are dates
    """
    assert counter in ['message', 'character', 'attachment']
    # get date range
    oldest = "9999-99-99"
    newest = "0000-00-00"
    for message in MESSAGES:
        timestamp = message['timestamp']
        date = datetime.fromisoformat(timestamp).strftime("%Y-%m-%d")
        oldest = min(date, oldest)
        newest = max(date, newest)
    headers = [oldest]
    while headers[-1] < newest:
        date = datetime.strptime(headers[-1], "%Y-%m-%d")
        date += timedelta(days=1)
        headers.append(date.strftime("%Y-%m-%d"))
    date_map = {}
    for i in range(len(headers)):
        date_map[headers[i]] = i
    # get data
    data = {}
    for message in MESSAGES:
        if attr not in ['author', 'channel']:
            continue
        if IGNORE_DELETED:
            if message['author']['discriminator'] == "0000":
                continue
        if attr == 'author':
            a = message[attr]
            username = '#'.join([a['username']] + [a['discriminator']]*(a['discriminator']!='0'))
            val = a['id']
            AUTHORS[val] = username
        if attr == 'channel':
            channelname = message['channel_name']
            val = message['channel_id']
            CHANNELS[val] = channelname
        if type(val) is not str:
            val = json.dumps(val)
        if val not in data:
            data[val] = [0] * len(headers)
        timestamp = message['timestamp']
        date = datetime.fromisoformat(timestamp).strftime("%Y-%m-%d")
        if counter == "message":
            data[val][date_map[date]] += 1
        if counter == "character":
            data[val][date_map[date]] += 1e-3*len(message['content'])
        if counter == "attachment":
            data[val][date_map[date]] += len(message['attachments'])
    return headers, data


def plot_count_date(attr_name, counter):
    """Generate a graph of message count vs. date for the top users"""
    dates, raw_data = generate_date_attr(attr_name, counter)
    dates = [datetime.strptime(date, "%Y-%m-%d") for date in dates]

    # get the PSA of message count
    data = []
    for (name, count) in raw_data.items():
        if attr_name == 'author':
            name = AUTHORS[name]
        if attr_name == 'channel':
            name = CHANNELS[name]

        count = list(map(float, count))

        # prefix sum array
        psa = count[:]
        for i in range(1, len(count)):
            psa[i] += psa[i-1]

        # truncate at the first nonzero
        ni = 0
        for c in count:
            if c > 0:
                break
            ni += 1
        ni = max(ni-1, len(count)-NUM_DAYS, 0)
        nj = len(count)
        for c in count[::-1]:
            if c > 0:
                break
            nj -= 1

        # apply
        data.append({
            'name': name,
            'dates': dates[ni:nj],
            'count': count[ni:nj],
            'psa': psa[ni:nj],
            'total': sum(count[ni:nj])
        })

    # get top values
    data = sorted(data, key=lambda _: -_['total'])
    if NUM_TOPS >= 0:
        data = data[:NUM_TOPS]
    num_days = max([len(d['dates']) for d in data])
    min_date = min([obj['dates'][0] for obj in data])
    max_date = max([obj['dates'][-1] for obj in data])

    for d in data:
        d['count'] = gaussian_filter(
            d['count'], 0.015*num_days, mode='nearest')

    # plot data
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    ax1.set_zorder(2)
    ax2.set_xlabel("Date")
    ax1.set_title(f"{counter.capitalize()} count,"
                  f" past {num_days} days")
    for (attr, ax, label) in zip(
        ['psa', 'count'], [ax1, ax2],
        ["culmulative", "daily"]
    ):
        if counter == 'character':
            label += ' (×1e3)'
        ax.set_ylabel(label)
        for obj in data:
            ax.plot(obj['dates'], obj[attr], label=obj['name'])
    ax1.legend(loc='upper left')
    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    ax2.xaxis.set_major_locator(mdates.DayLocator(interval=num_days//6))
    ax1.set_xlim([min_date, max_date])
    ax2.set_xlim([min_date, max_date])
    plt.gcf().autofmt_xdate()
    plt.show()


if __name__ == "__main__":
    guilds = [
        959874115311906957,  # EngSci 2T6
        1078486370252771369,  # EngSci 2T7
        1205550774277636159,  # EngSci 2T8
        1132786163225206904,  # DS101
    ]
    guilds = [1188335600126918736]  # spirulae
    load_messages(guilds)
    plot_count_date('channel', 'message')
    # plot_count_date('channel', 'character')
    plot_count_date('author', 'message')
    # plot_count_date('author', 'character')
    plot_count_date('channel', 'attachment')
