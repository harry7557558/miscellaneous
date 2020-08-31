# Text/code classfication for comment_string_directory.py
# Based on machine learning and SVM

from sklearn import svm
clf = svm.SVC(kernel='poly',degree=3,probability=True)


# convert a string to a number array for SVM
def str2array(s):
    # may affect accuracy but I assume it depends on coding habit
    s = s.strip()
    # manually handle "unusual" cases
    s = s.replace('...','.').replace('!!!','!').replace('???','?')
    while s.find('====')!=-1: s=s.replace('====','=')
    # count occurences of characters
    C = []
    l = max(len(s),1)
    C.append(1./l) # string length
    C.append(s.count(' ')/l)  # space count
    #C.append(s.count('\n'))  # line break count
    C.append(sum(['A'<=c<='Z' for c in s])/l)  # uppercase count
    C.append(sum(['a'<=c<='z' for c in s])/l)  # lowercase count
    C.append(sum(['0'<=c<='9' for c in s])/l)  # digit count
    #C += [s.count(c) for c in """!"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"""]
    C += [s.count(c)/l for c in """!#$&%.;<>@[\\]_`{|}~"""]
    #C.append(sum([ord(c)>127 for c in s]))  # non-ascii count
    return C


# print a string, and I tell the program if it is text or code
def manualTrain():
    s = eval(open('strings-copy.log','r').read())
    fi = eval('['+open("strings_train.log","r").read()+']')
    fp = open("strings_train.log",'a+')

    for i in range(len(fi),min(len(fi)+100,len(s))):
        print('[{0}]'.format(i))
        ss = s[i][1][0]+s[i][0]+s[i][1][1].rstrip('\n')
        print(ss)
        c = '' # text or code
        while not c in ['t','c']:
            c = input()
        fp.write(str(s[i]+[c])+', ')
        fp.flush()

    fp.close()


# test if a string is text by syntax
def isText_old(s, quotes=['','']):
    s = s.strip().replace('\n','')
    if not 6<len(s)<10000: return False
    ln = sum([s.lower().count(chr(c+97)) for c in range(26)])
    if ln<3: return False
    sm = sum([c in '''!#$&%.;<>@[\\]_`{|}~''' for c in s])
    coe = 10*len(s)**(-1.5)
    if 10<len(s) and sm/len(s)>max(min(coe,0.25),0.05):
        return False
    return True

# new method using SVM, requires clf to be initialized
def isText(s, quotes=['','']):
    s = s.strip()
    # handy cases
    if len(s)<3: return False
    if quotes in [['//','\n'],['#','\n'],['>','<']]:
        if s.count('-',0)<2 and s.replace('-','').rstrip(':').isalpha() and sum(['A'<=c<='Z' for c in s])<2:
            return True
    if quotes in [['//','\n'],['#','\n']]:
        if any([s.find(c*12)!=-1 for c in "=-+"]) and sum([c.isalpha() for c in s])>3:
            return True
    # SVM
    C = str2array(s)
    r = [dict(zip(clf.classes_, t)) for t in clf.predict_proba([C])][0]
    return r['t']>0.8*r['c']


# half data for training and the rest for testing
def testAccuracy():
    S = eval(open("strings_train.log",'r').read())
    N = len(S)//2

    SVs = []
    Cats = []
    for s in S:
        C = str2array(s[0])
        SVs.append(C)
        Cats.append(s[2])
    clf.fit(SVs[:N], Cats[:N])

    S = S[N:]
    r = [isText(S[i][0],S[i][1]) for i in range(N)]
    WAs = 0
    for i in range(N):
        ans = Cats[N:][i]
        if r[i]!=(ans=='t'):
            print('WA', 't' if r[i] else 'c', end='\t')
            print(S[i][1][0]+S[i][0]+S[i][1][1].strip('\n'))
            WAs += 1
    print('Accuracy: {0}'.format(1.-WAs/N))


# initialize SVM
def initSVM():
    S = eval(open("strings_train-copy.log",'r').read())
    SVs = [str2array(s[0]) for s in S]
    Cats = [s[2] for s in S]
    clf.fit(SVs, Cats)


