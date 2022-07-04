# Play a clip from the movie Frozen in a Discord chat

script = """
ANNA
Elsa? It's me...Anna?!

ELSA
Anna.

ANNA
Elsa, you look different....
It's a good different....
And this place is amazing.

ELSA
Thank you, I never knew what I was capable of.

ANNA
...I'm so sorry about what happened. If I'd known--

ELSA
No, it's okay. You don't have to apologize....
But you should probably go, please.

ANNA
But I just got here.

ELSA
...You belong in Arendelle.

ANNA
So do you.

ELSA
No, I belong here. Alone.
Where I can be who I am without hurting anybody.

ANNA
...Actually, about that--

OLAF
58...59...60.

ELSA
Wait. What is that?

OLAF
Hi, I'm Olaf and I like warm hugs.

ELSA
Olaf?

OLAF
You built me. You remember that?

ELSA
And you're alive?

OLAF
Um...I think so?

ANNA
He's just like the one we built as kids....
We were so close.
We can be like that again.

ELSA
No, we can't.

ELSA
Goodbye, Anna.

ANNA
Elsa, wait--

ELSA
I'm just trying to protect you.

ANNA
You don't have to protect me. I'm not afraid.
Please don't shut me out again.

ANNA
PLEASE DON'T SLAM THE DOOR.
YOU DON'T HAVE TO KEEP YOUR DISTANCE ANYMORE.

ANNA
`CAUSE FOR THE FIRST TIME IN FOREVER,
I FINALLY UNDERSTAND.
FOR THE FIRST TIME IN FOREVER,
WE CAN FIX THIS HAND IN HAND.
WE CAN HEAD DOWN THIS MOUNTAIN TOGETHER.
YOU DON'T HAVE TO LIVE IN FEAR.
`CAUSE FOR THE FIRST TIME IN FOREVER,
I WILL BE RIGHT HERE.

ELSA
Anna,
PLEASE GO BACK HOME.
YOUR LIFE AWAITS.
GO ENJOY THE SUN
AND OPEN UP THE GATES.

ANNA
Yeah, but--

ELSA
I know!
YOU MEAN WELL,
BUT LEAVE ME BE.
YES, I'M ALONE BUT I'M ALONE AND FREE.

ELSA
JUST STAY AWAY AND YOU'LL BE SAFE FROM ME.

ANNA
ACTUALLY, WE'RE NOT.

ELSA
WHAT DO YOU MEAN YOU'RE NOT?

ANNA
I GET THE FEELING YOU DON'T KNOW?

ELSA
WHAT DO I NOT KNOW?

ANNA
ARENDELLE'S IN DEEP DEEP DEEP DEEP SNOW.

ELSA
What?

ANNA
You kind of set off an eternal winter...
everywhere.

ELSA
Everywhere?

ANNA
It's okay, you can just unfreeze it.

ELSA
No, I can't. I don't know how.

ANNA
Sure you can. I know you can.

ANNA
CUZ FOR THE FIRST TIME IN FOREVER,

ELSA
I'M SUCH A FOOL!
I CAN'T BE FREE!

ANNA
YOU DON'T HAVE TO BE AFRAID.

ELSA
NO ESCAPE FROM THE STORM INSIDE OF ME!

ANNA
WE CAN WORK THIS OUT TOGETHER.

ELSA
I CAN'T CONTROL THE CURSE!

ANNA
WE'LL REVERSE THE STORM YOU'VE MADE.

ELSA
ANNA, PLEASE, YOU'LL ONLY MAKE ITWORSE!

ANNA
DON'T PANIC.

ELSA
THERE'S SO MUCH FEAR!

ANNA
WE'LL MAKE THE SUN SHINE BRIGHT.

ELSA
YOU'RE NOT SAFE HERE!

ANNA
WE CAN FACE THIS THING TOGETHER...

ELSA
NO!

ANNA
WE CAN CHANGE THIS WINTER WEATHER,
AND EVERYTHING WILL BE...

ELSA
I CAN'T!
""".strip().split('\n\n')

characters = {
    'Elsa': {
        'avatar': 'https://static.wikia.nocookie.net/disney/images/9/95/Profile_-_Elsa.jpeg/revision/latest/scale-to-width-down/516?cb=20200319054311',
    },
    'Anna': {
        'avatar': 'https://static.wikia.nocookie.net/disney/images/0/0f/Profile_-_Anna.jpeg/revision/latest/scale-to-width-down/516?cb=20200319054431',
    },
    'Olaf': {
        'avatar': 'https://static.wikia.nocookie.net/disney/images/5/53/Profile_-_Olaf.jpeg/revision/latest/scale-to-width-down/516?cb=20200221075027',
    }
}


import json
import requests
import time


with open(".webhooks", 'r') as fp:
    webhooks = json.load(fp)
    webhook = webhooks['TheatreBot']

contents = {
    'content': "",
    'username': None,
    'avatar_url': None
}

for sc in script:
    sc = sc.split('\n')
    char = sc[0].strip().capitalize()
    assert char in characters
    contents['username'] = char
    contents['avatar_url'] = characters[char]['avatar']
    for line in sc[1:]:
        print(char, '-', line)
        contents['content'] = line
        requests.post(webhook, data=contents)
        time.sleep(2)
