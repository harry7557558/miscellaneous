from sympy import *
import matplotlib.pyplot as plt

def p(n):
    return 1.0 - float(factorial(365)/factorial(365-n) / pow(365,n))

def p_log(n):
    return float(log(factorial(365)/factorial(365-n) / pow(365,n)) / log(10))

data_n = list(range(365+1))
data_p = [p(n) for n in data_n]

print(','.join([str((i,data_p[i])) for i in data_n]))
#print(','.join([str((i,p_log(i))) for i in range(365)]))

plt.xlabel('number of people')
plt.ylabel('probability')
plt.plot(data_n, data_p)
#plt.plot(data_n, data_p, "ro")
plt.show()
