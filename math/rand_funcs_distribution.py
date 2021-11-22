# inspired by https://www.shadertoy.com/view/NlV3Wz

# References:
# https://en.wikipedia.org/wiki/Convolution_of_probability_distributions
# https://en.wikipedia.org/wiki/Distribution_of_the_product_of_two_random_variables
# https://www.cl.cam.ac.uk/teaching/2003/Probability/prob11.pdf


import numpy as np
import matplotlib.pyplot as plt


N = 100000  # number of randoms
G = 100  # number of bins


def rnd_uni():
    """pdf: 1"""

    x = np.linspace(0.0, 1.0, G)

    r = np.random.random(N)
    p = np.ones(G)

    hist, bins = np.histogram(r, bins=x, density=True)
    bin_centers = 0.5*(x[1:]+x[:-1])
    plt.plot(bin_centers, hist)
    plt.plot(x, p)
    plt.show()


def rnd_add():
    """pdf: 2-4*abs(x-0.5)
    Convolution of probability functions"""

    x = np.linspace(0.0, 1.0, G)

    a = np.random.random(N)
    b = np.random.random(N)
    r = 0.5*(a+b)
    p = 2.0-4.0*np.abs(x-0.5)

    hist, bins = np.histogram(r, bins=x, density=True)
    bin_centers = 0.5*(x[1:]+x[:-1])
    plt.plot(bin_centers, hist)
    plt.plot(x, p)
    plt.show()


def rnd_mul1():
    """pdf: 1/(2sqrt(x))
    r(a)=a^2, dr=2ada=2sqrt(r)da, da=1/(2sqrt(r))dr"""

    x = np.linspace(0.0, 1.0, G)

    a = np.random.random(N)
    r = a*a
    p = 0.5/np.sqrt(x)

    hist, bins = np.histogram(r, bins=x, density=True)
    bin_centers = 0.5*(x[1:]+x[:-1])
    plt.plot(bin_centers, hist)
    plt.plot(x, p)
    plt.show()


def rnd_mul2():
    """pdf: -ln(x)
    r(y)=Integral[1/x,(x,y,1)]"""

    x = np.linspace(0.0, 1.0, G)

    a = np.random.random(N)
    b = np.random.random(N)
    r = a*b
    p = -np.log(x)

    hist, bins = np.histogram(r, bins=x, density=True)
    bin_centers = 0.5*(x[1:]+x[:-1])
    plt.plot(bin_centers, hist)
    plt.plot(x, p)
    plt.show()


def rnd_sqrt():
    """pdf: 2x
    r=sqrt(a), dr=1/(2sqrt(a))da=1/(2r)dr, da=2rdr"""

    x = np.linspace(0.0, 1.0, G)

    a = np.random.random(N)
    r = np.sqrt(a)
    p = 2.0*x

    hist, bins = np.histogram(r, bins=x, density=True)
    bin_centers = 0.5*(x[1:]+x[:-1])
    plt.plot(bin_centers, hist)
    plt.plot(x, p)
    plt.show()


def rnd_pow():
    """pdf: -16*ln(x)*x^3
    transform -ln(x) by x^0.25"""

    x = np.linspace(0.0, 1.0, G)

    a = np.random.random(N)
    b = np.random.random(N)
    r = pow(a*b, 0.25)
    p = -16.0*np.log(x)*pow(x,3)

    hist, bins = np.histogram(r, bins=x, density=True)
    bin_centers = 0.5*(x[1:]+x[:-1])
    plt.plot(bin_centers, hist)
    plt.plot(x, p)
    plt.show()


def rnd_max():
    """pdf: 2*x"""

    x = np.linspace(0.0, 1.0, G)

    a = np.random.random(N)
    b = np.random.random(N)
    r = np.maximum(a, b)
    p = 2.0*x

    hist, bins = np.histogram(r, bins=x, density=True)
    bin_centers = 0.5*(x[1:]+x[:-1])
    plt.plot(bin_centers, hist)
    plt.plot(x, p)
    plt.show()
    

def rnd_min():
    """pdf: 2-2*x"""

    x = np.linspace(0.0, 1.0, G)

    a = np.random.random(N)
    b = np.random.random(N)
    r = np.minimum(a, b)
    p = 2.0-2.0*x

    hist, bins = np.histogram(r, bins=x, density=True)
    bin_centers = 0.5*(x[1:]+x[:-1])
    plt.plot(bin_centers, hist)
    plt.plot(x, p)
    plt.show()


if __name__=="__main__":

    rnd_pow()
