# get comments/strings from source file

def extractText(s, PC):
    print("Detect", PC, '\n')
    ds = 0
    k = []
    while ds<len(s):
        md = len(s)
        mi = -1
        for i in range(len(PC)):
            d = s.find(PC[i][0], ds)
            if d!=-1 and d<=md:
                md, mi = d, i
        if mi!=-1:
            d0 = md+len(PC[mi][0])
            d = s.find(PC[mi][1], d0)
            if d==-1:
                print("Error: something wrong happens.\n")
                break
            #k.append(s[d0:d])
            k.append(PC[mi][0]+s[d0:d]+PC[mi][1].replace('\n',''))
            ds = d+len(PC[mi][1])
        else:
            ds=len(s)
    return k

def getCommentQuote(filename):
    PC = []
    lang = 0
    if any((s in ['.cs', '.cpp', '.cxx', '.c', '.h', '.hpp', '.inl', '.inc', '.java', '.jav']) for s in filename):
        lang = 1
    elif any((s in ['.py']) for s in filename):
        lang = 2
    elif any((s in ['.css', '.htm', '.html', '.shtml', '.shtm', '.js', '.xml']) for s in filename):
        lang = 3
    if lang==0:
        s = input("Select comment/string style  1 C/C++/Java  2 Python  3 HTML/CSS/JS : ")
        lang = int(s)
    if lang==1:
        PC = [['//','\n'], ['/*','*/'], ["'","'"], ['"','"']]
    elif lang==2:
        PC = [['#','\n'], ["'","'"], ['"','"'], ["'''","'''"], ['"""','"""']]
    elif lang==3:
        PC = [["<!--","-->"], ['/*','*/'], ['//','\n'], ["'","'"], ['"','"']]
    return PC


while True:
    filename = input('Enter source filename: ')
    try:
        s = open(filename, 'r').read().replace('\r', '')
    except:
        print("Failed loading source file.\n")
        continue
    PC = getCommentQuote(filename)
    k = extractText(s, PC)
    print('\n'.join(k))
    print('\n')


