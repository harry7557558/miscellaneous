# FFT circular convolution test
# Circular convolution of evenly spaced discrete samples in [0, 1]

import numpy as np
import matplotlib.pyplot as plt

from time import perf_counter


N = 1024


def base_fun(x):
    x = abs(x%1.0)
    return 0.5+x if x < 0.5 else 0.0


def conv_fun(x):
    x = abs(x)%1.0
    if 1:  # symmetrical/asymmetrical
        if x > 0.5:
            x = 1.0 - x
    sigma = 0.08
    s = 0.0
    for i in range(32):
        s += np.exp(-(i+x)**2/(2*sigma**2))/(np.sqrt(2*np.pi)*sigma)
    return s/N


def conv_bruteforce(x, y0):
    w = [conv_fun(x[j]-x[0]) for j in range(N)]
    y1 = np.zeros((N,))
    for k in range(N):
        s = 0.0
        for t in range(N):
            s += w[t-k] * y0[t]
        y1[k] = s
    return y1


def conv_fft(x, y0):
    w = [conv_fun(x[j]-x[0]) for j in range(N)]
    w = np.fft.fft(w)
    w = [w[-i] for i in range(N)]
    f0 = np.fft.fft(y0)
    f1 = w * f0
    y1 = np.fft.ifft(f1)
    return y1.real


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
