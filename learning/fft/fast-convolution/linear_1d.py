# FFT linear convolution test
# Linear convolution of evenly spaced discrete samples in [0, 1]

import numpy as np
import matplotlib.pyplot as plt

from time import perf_counter


N = 1024


def base_fun(x):
    return 2.0*x-0.2 if 0.4 < x < 0.6 else 0.0


def conv_fun(x):
    sigma = 0.2
    sigma = 0.03
    s = np.exp(-x**2/(2*sigma**2))/(np.sqrt(2*np.pi)*sigma)
    if 1:  # make it asymmetrical
        s *= 1+x/sigma
    return s/N


def conv_reference(x, y0):
    y1 = np.zeros((N,))
    for k in range(N):
        s = 0.0
        for t in range(N):
            w = conv_fun(x[k]-x[t])
            s += w * y0[t]
        y1[k] = s
    return y1


def conv_bruteforce(x, y0):
    w = [conv_fun((j-N)/N) for j in range(2*N)]  # a cheap method
    y1 = np.zeros((N,))
    for k in range(N):
        s = 0.0
        for t in range(N):
            s += w[k-t+N] * y0[t]
        y1[k] = s
    return y1


def conv_fft(x, y0):
    w = [conv_fun((j-N)/N) for j in range(2*N)]
    y0 = np.array([0.0 if t >= N else y0[t] for t in range(2*N)])
    # w = [w[(k+N)%(2*N)] for k in range(2*N)]
    w = np.fft.fft(w)
    w *= [(-1)**k for k in range(2*N)]  # shift by N
    f0 = np.fft.fft(y0)
    f1 = w * f0
    y1 = np.fft.ifft(f1)
    return y1.real[:N]


x = (np.arange(N)+0.5)/N
y0 = np.array([base_fun(t) for t in x])

t0 = perf_counter()
y1_bf = conv_bruteforce(x, y0)
dt = perf_counter()-t0
print("O(N^2):", round(1000*dt), "ms")

t0 = perf_counter()
y1_fft = conv_fft(x, y0)
dt = perf_counter()-t0
print("FFT:", round(1000*dt), "ms")

print("Error:", np.sqrt(sum((y1_bf-y1_fft)**2)))


plt.clf()
plt.plot(x, y0)
plt.plot(x, y1_bf)
plt.plot(x, y1_fft)
plt.show()
