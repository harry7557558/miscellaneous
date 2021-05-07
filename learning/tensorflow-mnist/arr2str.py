# convert array to string for hard-coding weights

def arr_to_str_1d(arr):
    s = []
    for i in range(len(arr)):
        t = "{:.3f}".format(arr[i])
        while t[0] == '0':
            t = t[1:]
        while t[0] == '-' and t[1] == '0':
            t = '-' + t[2:]
        s.append(t)
    return '[' + ",".join(s) + ']'


def arr_to_str_2d(arr):
    s = []
    for i in range(len(arr)):
        s.append(arr_to_str_1d(arr[i]))
    return '[' + ','.join(s) + ']'
