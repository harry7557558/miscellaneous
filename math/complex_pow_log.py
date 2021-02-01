# explore power/log/sqrt identities with complex numbers

from math import pi
from cmath import exp, log, sqrt

# random number generator
# all return complex number although the imaginary part may be zero
import random
rand = random.random
random.seed(1)
def randPositive():
    return -log(1-rand())/log(2)
def randNegative():
    return -randPositive()
def randNonNegative():
    return randPositive() if rand()>0.1 else 0
def randReal():
    return randPositive() if rand()<0.5 else randNegative()
def randComplex():
    return randPositive()*exp(2j*pi*rand())
def randComplexPositive():
    r = randPositive()*exp(2j*pi*rand())
    return abs(r.real)+r.imag*1j
def randComplexPI():
    return randPositive() + 2.j*pi*(rand()-0.5)
def randGeneral():
    x = rand()
    if x>0.4: return randComplex()
    if x<0.18: return randNegative()
    if x<0.36: return randPositive()
    return 0 if x<0.38 else 1

def diff(a,b):
    return min(abs(a-b), abs(a/b-1))
def realdiff(a,b):
    return min(abs(a.real-b.real), abs(a.real/b.real-1))
def absdiff(a,b):
    return min(abs(abs(a)-abs(b)), abs(abs(a)/abs(b)-1))

N = 1000
bad = []

for i in range(N):
    a = randReal()
    b = randPositive()
    x = randComplex()
    y = randGeneral()

    try:
        #ok = diff( abs(x*y), abs(x)*abs(y) )
        #ok = diff( pow(a,x), exp(x*log(a)) )
        #ok = diff(1/x, exp(-log(x)))
        #ok = diff( pow(a,0), 1 )
        #ok = diff( pow(a,-x), 1/pow(a,x) )
        #ok = diff( pow(a,x)*pow(a,y), pow(a,x+y))
        #ok = diff( pow(a,x)/pow(a,y), pow(a,x-y))
        #ok = diff( pow(pow(a,x),y), pow(a,x*y) )
        #ok = diff( pow(a*b,x), pow(a,x)*pow(b,x) )
        #ok = diff( pow(a/b,x), pow(a,x)/pow(b,x) )
        #ok = diff( sqrt(a)*sqrt(b), sqrt(a*b) )
        #ok = diff( sqrt(a)/sqrt(b), sqrt(a/b) )
        #ok = diff( 1/sqrt(a), sqrt(1/a) )
        #ok = diff( x, pow(a,log(x)/log(a)) )
        #ok = diff( log(exp(x)), x )
        #ok = diff( exp(log(x)), x )
        #ok = diff( log(x*y), log(x)+log(y) )
        #ok = realdiff( log(x/y), log(x)-log(y) )
        #ok = diff( log(pow(x,a)), a*log(x) )
        ok = diff( log(sqrt(x)), 0.5*log(x) )
    except:
        ok = float('nan')

    if not ok<1e-8:
        bad.append((ok,a,x))
        #bad.append((ok,x,y))

for s in bad: print(s)
print(len(bad)/N)
