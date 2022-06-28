# Generate and plot message statistics
# Run `fetch_messages.py` to generate `.messages.json`

import json
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


with open(".messages.json", "r") as fp:
    MESSAGES = json.load(fp)


def generate_date_attr(attr: str, ignore_deleted: bool):
    """Generate a graph of attribute vs. date
        Attribute is the dictionary key, can be 'author' or 'channel_name'
        Returns a table where the rows are dictionaries and columns are dates
    """
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
        if ignore_deleted:
            if message['author']['discriminator'] == "0000":
                continue
        val = message[attr]
        if type(val) is not str:
            val = json.dumps(val)
        if val not in data:
            data[val] = [0] * len(headers)
        timestamp = message['timestamp']
        date = datetime.fromisoformat(timestamp).strftime("%Y-%m-%d")
        data[val][date_map[date]] += 1
        #data[val][date_map[date]] += len(message['content'])
    return headers, data


def plot_user_count_date(num_users: int=-1, ignore_deleted=True):
    """Generate a graph of message count vs. date for the top users"""
    dates, raw_data = generate_date_attr('author', ignore_deleted)
    dates = [datetime.strptime(date, "%Y-%m-%d") for date in dates]
    # get the PSA of message count
    data = []
    for (key, count) in raw_data.items():
        author = json.loads(key)
        author = f"{author['username']}#{author['discriminator']}"
        for i in range(1, len(count)):
            count[i] += count[i-1]
        data.append({
            'author': author,
            'count': count
        })
    # get top users
    data = sorted(data, key=lambda _: -_['count'][-1])
    if num_users >= 0:
        data = data[:num_users]
    # plot data
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=90))
    for user in data:
        ni = 0
        for c in user['count']:
            if c > 0:
                break
            ni += 1
        ni = max(ni-1, 0)
        plt.plot(dates[ni:], user['count'][ni:], label=user['author'])
    plt.legend()
    plt.gcf().autofmt_xdate()
    plt.show()


def plot_channel_count_date(num_channels: int=-1, ignore_deleted=False):
    """Generate a graph of message count vs. date for top channels"""
    dates, raw_data = generate_date_attr('channel_name', ignore_deleted)
    dates = [datetime.strptime(date, "%Y-%m-%d") for date in dates]
    # get the PSA of message count
    data = []
    for (channel, count) in raw_data.items():
        for i in range(1, len(count)):
            count[i] += count[i-1]
        data.append({
            'channel': channel,
            'count': count
        })
    # get top channels
    data = sorted(data, key=lambda _: -_['count'][-1])
    if num_channels >= 0:
        data = data[:num_channels]
    # plot data
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=90))
    for channel in data:
        ni = 0
        for c in channel['count']:
            if c > 0:
                break
            ni += 1
        ni = max(ni-1, 0)
        plt.plot(dates[ni:], channel['count'][ni:], label=channel['channel'])
    plt.legend()
    plt.gcf().autofmt_xdate()
    plt.show()


if __name__ == "__main__":
    #print(MESSAGES[-1])
    count = 10
    plot_user_count_date(count, False)
    plot_channel_count_date(count)
