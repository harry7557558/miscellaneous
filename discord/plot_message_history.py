# Generate and plot message statistics
# Run `fetch_messages.py` to generate `.messages.json`

import json
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from scipy.ndimage import gaussian_filter


MESSAGES = []

def load_messages(guild_id=None):
    global MESSAGES

    if guild_id is None or len(guild_id) == 0:
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
NUM_DAYS = 720
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
    oldest = np.inf
    newest = -np.inf
    for message in MESSAGES:
        timestamp = message['timestamp']
        timestamp = datetime.timestamp(datetime.fromisoformat(timestamp))
        oldest = min(timestamp, oldest)
        newest = max(timestamp, newest)
    oldest = max(oldest, newest-NUM_DAYS*86400)
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
            data[val] = []
        timestamp = message['timestamp']
        timestamp = datetime.timestamp(datetime.fromisoformat(timestamp))
        delta = 0
        if counter == "message":
            delta = 1
        if counter == "character":
            delta = 1e-3*len(message['content'])
        if counter == "attachment":
            delta = len(message['attachments'])
        if delta != 0.0:
            data[val].append((timestamp, delta))
    data_out = {}
    for key in data:
        row = sorted(data[key], key=lambda _: _[0])
        if len(row) > 0:
            row = np.array(row, dtype=np.double)
            data_out[key] = (row[:,0], row[:,1])
    return (oldest, newest), data_out


def plot_count_date(attr_name, counter):
    """Generate a graph of message count vs. date for the top users"""
    (oldest, newest), raw_data = generate_date_attr(attr_name, counter)

    n = 1000
    dates = np.linspace(oldest, newest, n)
    num_days = (newest-oldest) / 86400

    # get the PSA of message count
    data = []
    for name, (timestamp, delta) in raw_data.items():
        if attr_name == 'author':
            name = AUTHORS[name]
        if attr_name == 'channel':
            name = CHANNELS[name]

        mask = timestamp > oldest
        timestamp = timestamp[mask]
        delta_after = delta[mask]
        delta_before = delta[~mask]
        counts = np.concatenate(([0.0], np.cumsum(delta_after))) + np.sum(delta_before)
        if len(timestamp) == 0:
            continue

        ts0, ts1 = np.amin(timestamp), np.amax(timestamp)
        if len(delta_before) > 0:
            ts0 = oldest
        m = int((ts1-ts0)/(newest-oldest)*n)+1
        dates_r = np.linspace(ts0, ts1, m)
        delta_r = np.zeros(m, dtype=np.double)
        if ts0 == ts1:
            delta_r += delta_after
        else:
            idx = np.floor((m-0.01)*(timestamp-ts0)/(ts1-ts0)).astype(np.int32)
            for i, d in zip(idx, delta_after):
                delta_r[i] += d

        # apply
        data.append({
            'name': name,
            'timestamps': timestamp,
            'deltas': delta_r * n / num_days,
            'dates': dates_r,
            'psa': counts[1:],
            'total': np.sum(delta_after)
        })

    # get top values
    data = sorted(data, key=lambda _: -_['total'])
    if NUM_TOPS >= 0:
        data = data[:NUM_TOPS]
    # min_date = min([obj['dates'][0] for obj in data])
    # max_date = max([obj['dates'][-1] for obj in data])

    for d in data:
        d['deltas'] = gaussian_filter(
            d['deltas'], 0.015*n, mode='reflect')

    # plot data
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    ax1.set_zorder(2)
    ax2.set_xlabel("Date")
    ax1.set_title(f"{counter.capitalize()} count,"
                  f" past {int(num_days+0.99)} days")
    for (attr, ax, label, tlabel) in zip(
        ['psa', 'deltas'], [ax1, ax2],
        ["culmulative", "daily"],
        ["timestamps", "dates"],
    ):
        if counter == 'character':
            label += ' (×1e3)'
        ax.set_ylabel(label)
        for obj in data:
            # dates = mdates.epoch2num(obj['timestamps'])
            dates = [datetime.fromtimestamp(t) for t in obj[tlabel]]
            ax.plot(dates, obj[attr], label=obj['name'])
    ax1.legend(loc='upper left')
    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    ax2.xaxis.set_major_locator(mdates.DayLocator(interval=int(num_days/8)+1))
    min_date = datetime.fromtimestamp(oldest)
    max_date = datetime.fromtimestamp(newest)
    ax1.set_xlim([min_date, max_date])
    ax2.set_xlim([min_date, max_date])
    # ax1.grid()
    # ax2.grid()
    plt.gcf().autofmt_xdate()
    plt.show()


if __name__ == "__main__":
    guilds = [
        959874115311906957,  # EngSci 2T6
        1078486370252771369,  # EngSci 2T7
        1205550774277636159,  # EngSci 2T8
        1132786163225206904,  # DS101
    ]
    guilds = [959874115311906957]  # EngSci 2T6
    # guilds = [1188335600126918736]  # spirulae
    load_messages(guilds)
    plot_count_date('channel', 'message')
    # plot_count_date('channel', 'character')
    plot_count_date('author', 'message')
    # plot_count_date('author', 'character')
    plot_count_date('channel', 'attachment')
    # plot_count_date('author', 'attachment')
