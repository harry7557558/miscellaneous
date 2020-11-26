# calculate the coefficients of the polynomial
# $P(x)=\sum_{k=0}^{x}{k^N}$  for N>=1
# return integer coefficients in increasing power and the denominator
def calcCoes(N):
    from math import gcd
    N += 1  # degree of the polynomial
    # initialize vector
    Y = [0]
    for i in range(1,N+1):
        Y.append(Y[-1]+i**(N-1))
    # initialize matrix
    A = []
    for i in range(0,N+1):
        A.append([i**e for e in range(N+1)])

    # elimination
    for i in range(N+1):
        Ai = A[i]
        for j in range(0,N+1):
            if j!=i:
                Aj = A[j]
                Aii,Aji = Ai[i],Aj[i]
                # prevent performance issue caused by large integers
                g = gcd(Aii,Aji)
                Aii,Aji=Aii//g,Aji//g
                # row transform
                for k in range(0,N+1):
                    Aj[k] = Aj[k]*Aii-Ai[k]*Aji
                Y[j] = Y[j]*Aii-Y[i]*Aji

    # make fractions
    lcm = lambda a,b: a*b//gcd(a,b)
    for i in range(N+1):
        s = gcd(A[i][i],Y[i])
        A[i][i]//=s
        Y[i]//=s
    den = 1  # denominator
    for i in range(N+1):
        den = lcm(den,A[i][i])
    X = [Y[i]*den//A[i][i] for i in range(N+1)]
    return [X,den]


# format polynomial coefficients to string
def printPolynomial(C):
    s = ''
    for i in range(len(C)-1,-1,-1):
        s += (C[i]!=0)*((C[i]>0 and len(s)>0)*'+'+str(C[i])+(i!=0)*('x'+(i!=1)*('^{'+str(i)+'}')))
    return s.replace('1x','x')

# format the result of calcCoes() as string
def printCoes(C_den):
    C,den = C_den
    N = len(C)-1
    s = (den!=1)*('\\frac{1}{'+str(den)+'}')
    s += '\\left(' + printPolynomial(C) + '\\right)'
    return s

# factor the polynomial
def printFactors(C_den):
    C,den = C_den
    N = len(C)-1
    
    import sympy
    x = sympy.Symbol('x')
    p = 0
    for i in range(N+1):
        p += C[i]*x**i
    p = sympy.factor(p)
    s = str(p)

    import re
    s = s.replace(' ','')
    s = re.sub('\*\*([0-9]+)','^{\\1}',s)
    s = s.replace('*','')
    s = s.replace('(','\\left(').replace(')','\\right)')
    return (den!=1)*('\\frac{1}{'+str(den)+'}') + s
    


# output

fp = open('sumpow.html','w')
fp.write('<script id="mathjax-config-script" type="text/x-mathjax-config">MathJax.Hub.Config({tex2jax:{inlineMath:[["$","$"]],preview:"none"},"fast-preview":{disabled:"true"},AssistiveMML:{disabled:true},menuSettings:{inTabOrder:false},messageStyle:"simple",positionToHash:false});</script><script async src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script>')

for i in range(1,20+1):
    s = '\\displaystyle{'
    s += '\\sum_{k=1}^{n}k^{'+str(i)+'}'
    C = calcCoes(i)
    s += '='+printCoes(C).replace('x','n')
    s += '='+printFactors(C).replace('x','n')
    s += '}'
    fp.write('$'+s+'$<br>')

fp.close()




