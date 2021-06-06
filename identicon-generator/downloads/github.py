import requests
import os

from PIL import Image
import numpy as np

for i in range(1000):
    _id = str(1000000+i)
    s = 'https://avatars.githubusercontent.com/u/'+_id
    r = requests.get(s, auth=('user', 'pass'))
    if r.status_code==200:
        filename = "github/"+_id+".png"
        with open(filename, 'wb') as fp:
            for c in r:
                fp.write(c)
        data = np.array(Image.open(filename))
        if data.shape!=(420,420,3) or np.count_nonzero(data.max(2)==240)<4096:
            os.remove(filename)
    else:
        print(r.status_code)
