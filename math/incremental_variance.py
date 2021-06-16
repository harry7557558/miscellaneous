import numpy as np
import matplotlib.pyplot as plt


class IncrementalVariance():

    def __init__(self):
        self.n = 0
        self.sx = 0.0
        self.sx2 = 0.0

    def add_element(self, x):
        self.n += 1
        self.sx += x
        self.sx2 += x*x

    def getmean(self):
        return self.sx / self.n

    def getvar(self):
        return (self.sx2 - self.sx**2/self.n) / max(self.n-1,1)


def variance_bruteforce(arr):
    avr = sum(arr)/len(arr)
    var = sum([(x-avr)**2 for x in arr]) / max(len(arr)-1,1)
    return var


def variance_incremental(arr):
    varcnt = IncrementalVariance()
    for x in arr:
        varcnt.add_element(x)
    return varcnt.getvar()


def test_calculation():
    arr = np.random.normal(loc=10.0, scale=2.0, size=(1000))
    print(variance_bruteforce(arr))
    print(variance_incremental(arr))


def test_convergence():
    BATCH_N = 1000
    BATCH_SIZE = 1000
    vals = [0]*BATCH_SIZE
    for batch in range(BATCH_N):
        arr = np.random.normal(loc=10.0, scale=2.0, size=(BATCH_SIZE))
        varcnt = IncrementalVariance()
        for i in range(BATCH_SIZE):
            varcnt.add_element(arr[i])
            vals[i] += varcnt.getvar()/BATCH_N
    plt.plot([0, BATCH_SIZE],[4.0, 4.0])
    plt.plot(vals[2:])
    plt.show()


if __name__=="__main__":
    test_calculation()
    test_convergence()
