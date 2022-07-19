# Try to distribute points on a unit sphere that minimizes repulsion

# Results:
# 2 points: linear
# 3 points: trigonal planar
# 4 points: tetrahedral
# 5 points: an equilateral triangle with two points on each side
# 6 points: octahedral, a square with two points on each side
# 7 points: a regular pentagon with two points on each side
# 8 points: two squares layed on top skewed 45 degrees
# 9 points: a point on top, a distorted pentagon in the middle, a triangle at the bottom (not exactly flat)
#           which is different from what I found on Google - https://en.wikipedia.org/wiki/Tricapped_trigonal_prismatic_molecular_geometry

# The result for higher number of points may be inaccurate
# due to penalty bias and difficulty of optimizing in high dimensions.


import numpy as np
import scipy.optimize


def calc_energy(ps):
    n = len(ps)//3+1
    ps = ps[:3*(n-1)].reshape((n-1, 3))  # reshape
    ps = np.concatenate(([[0.0, 0.0, 1.0]], ps))  # add first point
    # energy of repulsion
    er = 0.0
    for i in range(n):
        for j in range(i):
            # electric potential ?
            er += 1.0 / np.linalg.norm(ps[j]-ps[i])
    # penalty to force them on a unit sphere
    ea = 0.0
    for i in range(n):
        ea += 100. * (np.dot(ps[i], ps[i])-1.0)**2
    return er + ea


def calc_config(n: int):
    # initialize a fibonacci sphere
    # exclude the first point, which is (0, 0, 1)
    points = []
    for i in range(1, n):
        theta = 2.39996322973*i
        z = 2.0*(i+0.5)/n-1.0
        x = np.sqrt(1.0-z*z)*np.cos(theta)
        y = np.sqrt(1.0-z*z)*np.sin(theta)
        points += [x, y, z]
    # minimize repulsion
    opt = scipy.optimize.minimize(
        calc_energy, points)
    points = np.concatenate((
        [[0.0, 0.0, 1.0]],
        opt.x.reshape((n-1, 3))
    ))
    return points


def main():
    # calculate configurations from 2 to 16
    # inspired by the electron configuration of hybridized orbitals
    points = []
    for n in range(2, 16+1):
        print(n)
        ps = calc_config(n)
        ps = 0.25 * ps + [n, 0, 0]
        points += ps.tolist()

    # output for GeoGebra
    s = []
    for p in points:
        p = ','.join(["{:.3f}".format(c) for c in p])
        s.append(f"({p})")
    s = "{" + ','.join(s) + "}"
    print(s)


if __name__ == "__main__":
    main()
