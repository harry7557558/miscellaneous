# Extrude text contents in code directory for spelling/grammar check
# Requires source files to be UTF-8 encoding

# To-do:
# Rewrite the function below using AI ↓↓↓↓↓↓

# test if a commented string is English text
def isText(s, quotes=['','']):
    # the two cases: no doubt
    if s.replace('\n','').strip()=='': return False
    if not any(c.isalpha() for c in s): return False
    # works bad
    s = s.strip().replace('\n','').replace('...','.')
    if not 6<len(s)<10000: return False
    ln = sum([s.lower().count(chr(c+97)) for c in range(26)])
    if ln<3: return False
    sm = sum([c in '''!#$&%.;<>@[\\]_`{|}~''' for c in s])
    coe = 10*len(s)**(-1.5)
    if 10<len(s) and sm/len(s)>max(min(coe,0.25),0.05):
        return False
    return True



import os

# list all files in a directory
def searchDirectory(_dir):
    ls = [f for f in os.listdir(_dir) if f[0]!='.']
    files = [_dir+f for f in ls if os.path.isfile(_dir+f)]
    dirs = [_dir+f+'\\' for f in ls if os.path.isdir(_dir+f)]
    for path in dirs:
        files += searchDirectory(path)
    # remove binary/developing files by filtering file extensions
    # VC can sometimes be ****
    def isValid(fn):
        if any([fn.find(u)!=-1 for u in ['.vcxproj','.tlog']]): return False
        ext = fn.rsplit('.',1)[-1].lower()
        if ext in ['lnk','sln','exe','dll','ilk','pdb','iobj','ipdb','pdb','obj','idb','enc','pch','sdf','suo','log','dat','pyc','pyw']: return False
        if ext in ['png','gif','bmp','jpg','psd','ai','ico','stl','ply','blend','pdf','doc','docx','zip','rar','tar','gz']: return False
        return True
    return [f for f in files if isValid(f)]

# read utf-8 file, preserves BOM and line ending
def readFile(filename):
    if os.path.getsize(filename)>2**20:  # 1MB size limit
        return ''
    try: return str(open(filename,'rb').read(),'utf-8')
    except: return ''

# detect line ending, return readable string
def lineEnding(s):
    crlf = s.count('\r\n')
    lf = s.count('\n') - crlf
    cr = s.count('\r') - crlf
    if crlf|lf|cr==0:
        return ''
    q = ' ({0},{1},{2})'.format(lf,cr,crlf)*((crlf!=0)+(cr!=0)+(lf!=0)!=1)
    e = '\\r\\n' if crlf>max(cr,lf) else ('\\n' if cr<lf else '\\r')
    return "Line ending: " + e + q + '\n'

# text extruding main function, return readable message
def checkFile(filename):
    # get code content
    s = readFile(filename)
    if s == '' or (len(s)>65536 and s.count('\n')<50):
        return 'Ignored\n'
    msg = ''
    msg += (ord(s[0])==65279)*'UTF-8 BOM detected\n'
    msg += lineEnding(s)
    s = s.lstrip(chr(65279)).replace('\r\n', '\n')
    s = s.replace('\t', '    ')  # distinguish from tab after line number

    # guess comment quotes from file extension
    ext = filename.rsplit('.',1)[-1].lower()
    lang = ''
    quotes = []
    QUOTES_STR = [["'","'"],['"','"']]
    QUOTES_C = [['/*','*/'], ['//','\n']] + QUOTES_STR
    QUOTES_P = [['#','\n'], ["'''","'''"], ['"""','"""']] + QUOTES_STR
    QUOTES_X = [['‹‹!--','--››'],['>','<']] + QUOTES_STR  # HTML is a big exception
    if ext in ['cs','cpp','cxx','c','h','hpp','inl','inc','java','jav','js','css']:
        lang, quotes = 'C', QUOTES_C
    if ext in ['py']:
        lang, quotes = 'Python', QUOTES_P
    if ext in ['htm','html','shtm','shtml','xhtm','xhtml','xml','svg']:
        lang, quotes = 'HTML', QUOTES_X

    DiscardedList = []

    # treat unsupported languages as plain text
    if quotes==[]:
        s = s.split('\n')
        for i in range(len(s)):
            st = s[i]
            if isText(st.strip()):
                msg += 'L'+str(i+1)+'\t'+st+'\n'
        return msg

    # most languages use quotes to represent string
    sq1, sq2, bkslash = ['❜','❞','⑊']  # very less-used characters
    s = s.replace('\\\\',bkslash).replace("\\'",sq1).replace('\\"',sq2)  # quotes in quoted string
    s = s.replace('<!--','‹‹!--').replace('-->','--››')  # hmmm...
    #quotes.sort(reverse=True,key=(lambda s: len(s[0])))
    s += '\n'

    # initialize a prefix sum array of lines (map index to line)
    line = []
    for i in s:
        if len(line)==0: line.append(1)
        else: line.append(line[-1]+int(i=='\n'))

    # search comments in code
    comments = []
    def checkScript(d0, d1):
        nonlocal lang, quotes
        
        while True:
            nonlocal msg
            
            # find the next comment
            md = d1
            quo = []
            for q in quotes:
                dd = s.find(q[0],d0)
                if dd!=-1 and dd<=md:
                    md=dd
                    quo=q
            if md==d1:
                break
            
            # find the closed comment pair
            dd = s.find(quo[1],md+len(quo[0]))
            if dd==-1:
                if quo[0]!='>':
                    msg += 'Unbalanced comment: L{0} {1}\n'.format(line[md],quo[0])
                break
            
            # add the comment
            ss = s[md+len(quo[0]):dd]
            if quo==['>','<'] and ss.find('‹')!=-1:  # fix html overriding
                lang, quotes = 'iHTML', [['‹!--','--›'],['>','‹'],['›','<']]
                checkScript(md,dd+1)
                lang, quotes = 'HTML', QUOTES_X
            elif isText(ss,quo):
                if quo[0]!='>' and quo[1]!='<':
                    ss = quo[0]+ss+quo[1]
                msg += 'L'+str(line[md])+'\t'+ss.strip('\n')+'\n'
            else:
                DiscardedList.append([line[md],ss.replace('\n','').replace('    ',' ')])
            d0 = dd+len(quo[1])
            
            # html special (may not always work)
            if lang=='HTML':
                lang, quotes = 'C', QUOTES_C
                if quo[1]=='<' and s[d0:d0+6]=='script':
                    md = s.find('</script>',d0)
                    checkScript(d0+6,md)
                    d0 = md
                elif quo[1]=='<' and s[d0:d0+5]=='style':
                    md = s.find('</style>',d0)
                    checkScript(d0+5,md)
                    d0 = md
                lang, quotes = 'HTML', QUOTES_X

    checkScript(0,len(s))
    
    #print(str(DiscardedList))
    msg = msg.replace(sq1,"\\'").replace(sq2,'\\"').replace(bkslash,'\\\\')
    msg = msg.replace('‹‹','<').replace('››','>').replace('‹','<').replace('›','>')
    return msg




_dir = 'D:\\Coding\\Github\\'

fs = searchDirectory(_dir)

fp = open("output.log","w")


for f in fs:
    s = readFile(f)
    print(f)
    fp.write(f+'\n')
    msg = checkFile(f)
    fp.write(msg+'\n')
    fp.flush()

fp.close()