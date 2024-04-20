# Generate and plot message statistics
# Run `fetch_messages.py` to generate `.messages.json`

import json
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy.ndimage import gaussian_filter
import re
import random
from collections import defaultdict


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


NUM_DAYS = 60
NUM_TOPS = 20


def get_messages_words(messages):
    content = []
    for m in messages:
        if 'content' in m and isinstance(m['content'], str):
            s = m['content'].strip()
            s = '\n'.join(s.split('```')[::2])
            if len(s) > 0:
                content.append(s)
    text = '\n'.join(content[:])
    print(len(text))

    stop_words = set([
        'i', 'the', 'to', 'a', 'and', 'is', 'in', 'it', 'of', 'you', 'that', 'for', 'not',
        'my', 'me', 'this', 'like', 'but', 'on', 'are', 'with', 'if', 'what', 'be', 'have',
        'no', 'just', 'can', 'so', 'was', 'or', 'do', 'one', 'they', "don't", 'he', 'there',
        "i'm", 'get', 'at', 'some', 'when', 's', 'from', 'also', 'will', 'how', 'more',
        'why', 'as', 'who', 'by', 'up', 'got', 'should', 'about', 'she', 'all', 'yes', 'want',
        'than', 'an', 'your', 'its', 'we', 'did', 'x', 'now', 'out', 'oh', 'y', 'too', 'go',
        'only', 'yeah', 'has', 'f', 'then', 'her', 'u', 'last', 'them', 'even', 'going',
        'would', 'much', "can't", 'ok', "didn't", 'am', 't', 'other', 'him', 'may', 'his',
        "i'll", '-', 'k', 'any', 'where', "doesn't", 'their', 'z', 'here', 'because', 'those',
        'many', 'had', 'which', "i've", 'were', 'ur', 'does', 'n', 'cuz', 'most', 'could', 'c',
        'use', 'being', 'getting', 'made', 'p', 'w', 'very', 'these', 'both', 'b', 'put', 'yo',
        'less', 'kinda', 'used', "isn't", 'im', 'us', 'every', 'while', 'next', 'over', 'might',
        'doing', 'thing', 'r', 'hi', 'thanks', 'thank', 'sorry', 'ones', 'take', 'set', 'ill',
        'lol', 'bro', 'tho', 'don', 'ye', 'nah', 'rn', 'ah', 'mhm', 'mm', 'hmm', 'gonna', 'wanna',
        'idk', 'lmao', 'done', 'yet', 'please', 'lot', 'lots', 'let', 'etc', 'isnt', 'cant', 'yea',
        'been', 'since', 'things', 'into', 'without', 'went', "you're", 'dont', 'thats', 'bruh',
        'didnt', 'wtf', 'hey', 'doesnt', 'each', 'gotta', 'else', 'blud', 'nvm', 'tbh', 'ngl',
        'hes', 'theres', 'okay', 'using', 'boutta', 'll', 'tf', 'taking', 'imma', 'whats', 'aint',
        'ya', 'fr', 'having', 'although', 'aight', 'such', 'didn', 'goes', 'gets', "won't", 'ig',
        'vs', 'away', 'tryna', 'ight', 'bc', 'theyre', 'few', 'btw', 'ty', 'bros', 'per', 'doesn',
        'uh', 'must', 'ive', 'takes', "haven't", 'under', 've', 'alr', 'yall', 'ik', "they're",
        'thx', 'isn', 'jus', 'bout', 'wants', "we're", 'ong', 'wont', "wasn't", "wouldn't",
        'wdym', 'cannot', 'ab', 'huh', "you'll", 'dw', 'non', 'smth', 'smt', 'mb', 'ohhh', "aren't",
        "alright", "couldn't", "lemme", "asf", 'idek', 'wouldnt', 'yup', 'omg', 'arent', 'ahh',
        'rlly', 'thru', 'wow', 'whos', "shouldn't", 'youre', 'imo', 'lmfao', 'irl', 'ohh', 'np',
        'doe', 'haha', 'okok', "y'all", 'ez', 'af', 'gg', 'gone', 'wat', 'op', 'ofc', 'um', 'couldnt',
        'yjk', 'sth', 'uhh', 'stfu', 'shes', 'iirc', "ain't", 'plz', 'lawl', 'shouldnt', 'smh',
        'youll', "we'll", 'eh', 'heh', 'tru', 'mf', 'mfs', 'st', 'xd', 'kn', 'jk', 'wouldn', 'rly',
        'ayo', 'uhhh', 'shall', "it'll", 'ain', 'wasn', 'lmaoo', 'hm', 'iii', 'kk', "they'll", 'la',
        'wut', 'ohhhh', 'hmmm', 'wym', 'dy', 'aka', "you've", 'thus', 'lolz', 'ant', 'th'
    ])

    word_freq = defaultdict(int)
    text = re.sub(
        r"((http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-]))",
        " ", text.lower())
    words = re.findall(r"\b['a-zA-Z-]+\b", text)
    all_words = []
    for word in words:
        word = re.sub(r"[^'a-zA-Z-]", '', word)
        word = re.sub(r"'(s|d|es|ed)$", '', word)
        if len(word) > 1 and word not in stop_words:
            word_freq[word] += 1
            all_words.append(word)
    word_freq = dict(word_freq)
    random.shuffle(all_words)

    print(len(word_freq))
    print(sorted(word_freq.items(), key=lambda _: -_[1])[:200])
    # print(','.join([_[0] for _ in sorted(word_freq.items(), key=lambda _: -_[1])[:2000]]))

    from wordcloud import WordCloud
    wc = WordCloud(background_color="white",
                   colormap="viridis",
                   width=1024, height=768,
                   max_font_size=80,
                   min_word_length=2)
    # wc.generate(text)
    wc.generate('\n'.join(all_words))
    wc.to_file("wordcloud.png")
    plt.figure()
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.show()





if __name__ == "__main__":
    guilds = [
        959874115311906957,  # EngSci 2T6
        1078486370252771369,  # EngSci 2T7
        1205550774277636159,  # EngSci 2T8
        1132786163225206904,  # DS101
    ]
    guilds = [1188335600126918736]  # spirulae
    # guilds = [1197229140886167582]  # ESC204
    load_messages(guilds)
    get_messages_words(MESSAGES)
