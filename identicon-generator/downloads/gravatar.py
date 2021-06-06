import requests

for i in range(1000):
    _id = str(i)
    s = 'http://www.gravatar.com/avatar/'+_id+'?d=identicon&s=256'
    r = requests.get(s, auth=('user', 'pass'))
    if r.status_code==200:
        with open("gravatar/"+_id+".png", 'wb') as fp:
            for c in r:
                fp.write(c)
    else:
        print(r.status_code)
