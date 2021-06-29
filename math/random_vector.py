# Generate random vectors with different probability distributions

import numpy as np
from random import random
import matplotlib.pyplot as plt
from math import sin, cos, pi, sqrt, exp, log, asin
import sympy


""" Random Functions """


# One-dimensional


def rand_trig_01():
    """ pdf(x) = 2*x if 0<x<1 else 0 """
    u = random()
    return sqrt(u)


def rand_trig_11():
    """ pdf(x) = 1-abs(x) if -1<x<1 else 0 """
    u = random()
    x = sqrt(2*u)-1 if u<0.5 else -sqrt(2-2*u)+1
    return x


def rand_normal_1d(mu, sigma):
    """ standard normal distribution with given mean and standard deviation """
    def inverf(x):
        n = log(1-x*x)
        t = 0.5*n + 2/(0.147*pi)
        v = sqrt(-t + sqrt(t*t-n/0.147))
        return -v if x<0 else v
    p = random()
    return mu + sqrt(2)*sigma * inverf(2*p-1)


def rand_exp_1d(lambda_):
    """ pdf(x) = λ*exp(-λ*x) if x>0 else 0 """
    p = random()
    return -log(1-p)/lambda_


# 2D Area


def rand_disk_uniform():
    """ uniformly random inside an unit circle
        pdf(x,y) = 1/π if x²+y²<1 else 0 """
    u = 2*pi * random()
    v = random()
    d = sqrt(v)
    x = d*cos(u)
    y = d*sin(u)
    return [x, y]


def rand_disk_cone():
    """ pdf(x,y) = 3/pi * (1-sqrt(x²+y²)) if x²+y²<1 else 0 """
    u = 2*pi * random()
    v = random()
    #d = np.roots([2, -3, 0, v])[1]
    d = 0.5-sin(asin(1.0-2.0*v)/3.0)  # inverse smoothstep
    x = d*cos(u)
    y = d*sin(u)
    return [x, y]


def rand_disk_concentric(r0, r1):
    """ uniformly random inside r0<sqrt(x²+y²)<r1 """
    u = 2*pi * random()
    v = random()
    r = sqrt(r0**2 + (r1**2-r0**2)*v)
    x = r*cos(u)
    y = r*sin(u)
    return [x, y]


def rand_triangle():
    """ uniformly random in a triangle with vertice (0,0), (1,0), (0,1)
        no nonlinear transform involved """
    u = random()
    v = random()
    if u+v > 1:
        u, v = 1-u, 1-v
    return [u, v]


# 3D Surface


def rand_sphsurf_uniform():
    """ uniformly random on the surface of an unit sphere
        dP/dA = 1/(4π) """
    u = 2*pi * random()
    v = 2.0*random()-1.0  # φ=acos(v)
    r = sqrt(1-v*v)
    x = r*cos(u)
    y = r*sin(u)
    z = v
    return [x, y, z]


def rand_sphsurf_cosine():
    """ cosine distributed on a hemisphere
        dP/dA = 1/π * cos(φ) """
    u = 2*pi * random()
    v = random()  # φ=asin(√v)
    r = sqrt(v)
    x = r*cos(u)
    y = r*sin(u)
    z = sqrt(1-r*r)
    return [x, y, z]


def rand_sphsurf_angle(alpha):
    """ uniformly random on the surface of a solid angle
        on surface (sinφcosθ,sinφsinθ,cosφ) where 0<θ<2π and 0<φ<α """
    u = 2*pi * random()
    v = random()  # φ=acos(1-v*(1-cosα))
    z = 1-v*(1-cos(alpha))
    r = sqrt(1-z*z)
    x = r*cos(u)
    y = r*sin(u)
    return [x, y, z]


# 3D Volume

# Linear transformation may be applied to generated
# random points inside an ellipsoid/arbitrary cone


def rand_sphere_uniform():
    """ uniformly random inside an unit sphere
        pdf(x,y,z) = 3/(4π) if x²+y²+z²<1 else 0 """
    u = 2*pi * random()
    v = 2.0*random()-1.0  # cosφ
    w = random()
    sinφ = sqrt(1-v*v)
    r = w**(1/3)
    x = r*sinφ*cos(u)
    y = r*sinφ*sin(u)
    z = r*v
    return [x, y, z]


def rand_solidangle_uniform(alpha):
    """ uniformly random inside a solid angle
        on surface (r⋅sinφcosθ,r⋅sinφsinθ,r⋅cosφ) where 0<θ<2π, 0<φ<α, 0<r<1
        constraint: 0 < α < π """
    u = 2*pi * random()
    v = random()
    w = random()
    cosφ = 1-v*(1-cos(alpha))
    sinφ = sqrt(1-cosφ**2)
    r = w**(1/3)
    x = r*sinφ*cos(u)
    y = r*sinφ*sin(u)
    z = r*cosφ
    return [x, y, z]


def rand_cone_uniform():
    """ uniformly random inside an unit cone
        pdf(x,y,z) = 3/π if sqrt(x²+y²)<z<1 else 0 """
    u = 2*pi * random()
    v = random()
    w = random()
    r = sqrt(v)
    h = w**(1/3)
    x = h*r*cos(u)
    y = h*r*sin(u)
    z = h
    return [x, y, z]


def rand_sphere_concentric(r0, r1):
    """ uniformly random inside r0<sqrt(x²+y²+z²)<r1 """
    u = 2*pi * random()
    v = 2.0*random()-1.0
    w = random()
    r = (r0**3+(r1**3-r0**3)*w)**(1/3)
    sinφ = sqrt(1-v*v)
    x = r*sinφ*cos(u)
    y = r*sinφ*sin(u)
    z = r*v
    return [x, y, z]


""" Check if the formula is correct """

# Jacobian should be constant for the transformation of an uniform distribution


def rand_sphere_uniform_check():
    from sympy import sin, cos, sqrt, cbrt, Matrix
    u, v, w = sympy.symbols('u, v, w')
    x = cbrt(w)*sqrt(1-v**2)*cos(u)
    y = cbrt(w)*sqrt(1-v**2)*sin(u)
    z = cbrt(w)*v
    jacmat = Matrix([x, y, z]).jacobian(Matrix([u, v, w]))
    jac = sympy.simplify(jacmat.det())
    print(jac)  # 1/3


def rand_solidangle_uniform_check():
    from sympy import sin, cos, sqrt, cbrt, Matrix
    u, v, w, alpha = sympy.symbols('u, v, w, alpha')
    d = 1-v*(1-cos(alpha))
    x = cbrt(w)*sqrt(1-d*d)*cos(u)
    y = cbrt(w)*sqrt(1-d*d)*sin(u)
    z = cbrt(w)*d
    jacmat = Matrix([x, y, z]).jacobian(Matrix([u, v, w]))
    jac = sympy.simplify(jacmat.det())
    print(jac)  # cos(alpha)/3 - 1/3
    

def rand_cone_uniform_check():
    from sympy import sin, cos, sqrt, cbrt, Matrix
    u, v, w = sympy.symbols('u, v, w')
    x = cbrt(w)*sqrt(v)*cos(u)
    y = cbrt(w)*sqrt(v)*sin(u)
    z = cbrt(w)
    jacmat = Matrix([x, y, z]).jacobian(Matrix([u, v, w]))
    jac = sympy.simplify(jacmat.det())
    print(jac)  # -1/6


def rand_sphere_concentric_check():
    from sympy import sin, cos, sqrt, cbrt, Matrix
    u, v, w, r0, r1 = sympy.symbols('u, v, w, r0, r1')
    r = cbrt(r0**3+(r1**3-r0**3)*w)
    x = r*sqrt(1-v*v)*cos(u)
    y = r*sqrt(1-v*v)*sin(u)
    z = r*v
    jacmat = Matrix([x, y, z]).jacobian(Matrix([u, v, w]))
    jac = sympy.simplify(jacmat.det())
    print(jac)  # -r0**3/3 + r1**3/3


""" Tests """


def test_1d():

    N = 100000
    x = np.array([rand_trig_11() for i in range(N)])

    bins = np.linspace(-2, 2, 100)
    hist, bins = np.histogram(x, bins=bins, density=True)
    bin_centers = 0.5*(bins[1:]+bins[:-1])

    plt.plot(bin_centers, hist)
    plt.show()


def test_2d():

    N = 400000
    x = np.array([rand_disk_cone() for i in range(N)])

    bins = np.linspace(-2, 2, 41)
    hist, xedges, yedges = np.histogram2d(x[:, 0], x[:, 1], bins=(bins, bins), density=True)

    if 0:  # 2d colormap
        plt.imshow(hist, interpolation='nearest', origin='lower',
                   extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]])
    else:  # 3d plot
        ax = plt.figure().add_subplot(projection='3d', proj_type='ortho')
        x, y = np.meshgrid(0.5*(xedges[1:]+xedges[:-1]), 0.5*(yedges[1:]+yedges[:-1]))
        ax.plot_surface(x, y, hist)

    plt.show()


def test_3d():

    N = 1000
    x = np.array([rand_sphere_uniform() for i in range(N)])

    ax = plt.figure().add_subplot(projection='3d', proj_type='ortho')
    ax.set_box_aspect(np.ptp(x, axis=0))
    ax.scatter(x[:, 0], x[:, 1], x[:, 2])
    plt.show()


if __name__=="__main__":

    test_3d()
