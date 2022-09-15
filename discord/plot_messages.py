# Generate and plot message statistics
# Run `fetch_messages.py` to generate `.messages.json`

import json
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy.ndimage import gaussian_filter


with open(".messages.json", "r") as fp:
    MESSAGES = json.load(fp)

IGNORE_DELETED = False
NUM_DAYS = 180
NUM_TOPS = 10


def generate_date_attr(attr: str, counter: str):
    """Generate a graph of attribute vs. date
        Attribute is the dictionary key, can be 'author' or 'channel_name'
        Returns a table where the rows are dictionaries and columns are dates
    """
    assert counter in ['message', 'character']
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
        if attr not in message:
            continue
        if IGNORE_DELETED:
            if message['author']['discriminator'] == "0000":
                continue
        val = message[attr]
        if attr == 'author':
            a = message[attr]
            val = '#'.join([a['username'], a['discriminator']])
        if type(val) is not str:
            val = json.dumps(val)
        if val not in data:
            data[val] = [0] * len(headers)
        timestamp = message['timestamp']
        date = datetime.fromisoformat(timestamp).strftime("%Y-%m-%d")
        if counter == "message":
            data[val][date_map[date]] += 1
        if counter == "character":
            data[val][date_map[date]] += len(message['content'])
    return headers, data


def plot_count_date(attr_name, counter):
    """Generate a graph of message count vs. date for the top users"""
    dates, raw_data = generate_date_attr(attr_name, counter)
    dates = [datetime.strptime(date, "%Y-%m-%d") for date in dates]

    # get the PSA of message count
    data = []
    for (name, raw_count) in raw_data.items():
        raw_count = list(map(float, raw_count))

        # prefix sum array
        psa = raw_count[:]
        for i in range(1, len(raw_count)):
            psa[i] += psa[i-1]

        # daily number of messages
        count = gaussian_filter(raw_count, 0.02*NUM_DAYS, mode='reflect')

        # truncate at the first nonzero
        ni = 0
        for c in raw_count:
            if c > 1:
                break
            ni += 1
        ni = max(ni-1, len(raw_count)-NUM_DAYS, 0)

        # apply
        data.append({
            'name': name,
            'dates': dates[ni:],
            'count': count[ni:],
            'psa': psa[ni:],
            'total': sum(raw_count[ni:])
        })

    # get top values
    data = sorted(data, key=lambda _: -_['total'])
    if NUM_TOPS >= 0:
        data = data[:NUM_TOPS]

    # plot data
    fig, (ax1, ax2) = plt.subplots(2, 1)
    ax1.set_zorder(2)
    ax2.set_xlabel("Date")
    ax1.set_title(f"{counter.capitalize()} count by {attr_name} vs. date"
                  f" in the past {NUM_DAYS} days")
    for (attr, ax, label) in zip(
        ['psa', 'count'], [ax1, ax2],
        ["culmulative", "daily"]
    ):
        ax.set_ylabel(label)
        for obj in data:
            ax.plot(obj['dates'], obj[attr], label=obj['name'])
    ax1.legend(loc='upper left')
    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    ax2.xaxis.set_major_locator(mdates.DayLocator(interval=NUM_DAYS//6))
    plt.gcf().autofmt_xdate()
    plt.show()


if __name__ == "__main__":
    plot_count_date('channel_name', 'message')
    plot_count_date('channel_name', 'character')
    plot_count_date('author', 'message')
    plot_count_date('author', 'character')
