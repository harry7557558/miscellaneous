import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize
from math import gcd
from time import perf_counter

# planning parameters

pA = np.array([0, 0])
pB = np.array([1, 1])
ND, GR = 16, 2
INF = 10.0


def generateRandomCircles(nc, seed):
    np.random.seed(seed)
    PC = []
    RC = []
    while len(PC) < nc:
        p = np.random.random(2)
        r = 0.025+abs(np.random.normal(0, 0.05, size=1))
        if np.linalg.norm(p) > r and np.linalg.norm(p-[1,1]) > r:
            PC.append(p)
            RC.append(r)
    return np.array(PC), np.array(RC)


def generateGraph(PC, RC):

    # grid
    minp = np.min(np.concatenate([PC-RC, [pA, pB]]), axis=0)-0.25
    maxp = np.max(np.concatenate([PC+RC, [pA, pB]]), axis=0)+0.25
    vals = np.zeros((ND, ND))
    ps = np.zeros((ND, ND, 2))
    for i in range(ND):
        for j in range(ND):
            ps[i][j][0] = minp[0] + (maxp[0]-minp[0]) * i/(ND-1)
            ps[i][j][1] = minp[1] + (maxp[1]-minp[1]) * j/(ND-1)
            vals[i][j] = INF
            for p, r in zip(PC, RC):
                d = np.linalg.norm(p-ps[i][j]) - r
                vals[i][j] = min(vals[i][j], d)

    # neighbors
    def isOccluded(p0, p1):
        dp = p1 - p0
        for p, r in zip(PC, RC):
            op = p0 - p
            a = np.dot(dp, dp)
            b = np.dot(op, dp)
            c = np.dot(op, op) - r*r
            if c < 0:
                return True
            d = b*b-a*c
            if d < 0:
                continue
            if 0 <= -b-d**0.5 <= a:
                return True
            if 0 <= -b+d**0.5 <= a:
                return True
        return False

    nbs = [None]*(ND*ND)
    for i in range(ND):
        for j in range(ND):
            nbs[i*ND+j] = {}
            p0 = ps[i][j]
            for i1 in range(max(i-GR,0), min(i+GR+1,ND)):
                for j1 in range(max(j-GR,0), min(j+GR+1,ND)):
                    if gcd(i1-i, j1-j) != 1:
                        continue
                    p1 = ps[i1][j1]
                    if not isOccluded(p0, p1):
                        nbs[i*ND+j][i1*ND+j1] = np.linalg.norm(p1-p0)
    ps = ps.reshape((ND*ND, 2))

    # start/end
    ps = np.concatenate((ps, [pA, pB]))
    nbs += [{}, {}]
    iA = len(nbs) - 2
    iB = len(nbs) - 1
    th = 2.0*(maxp-minp)*GR/ND
    for i in range(ND*ND):
        if np.linalg.norm((ps[i]-pA)/th) < 1.0:
            if not isOccluded(ps[i], pA):
                d = np.linalg.norm(ps[i]-pA)
                nbs[i][iA] = d
                nbs[iA][i] = d
        if np.linalg.norm((ps[i]-pB)/th) < 1.0:
            if not isOccluded(ps[i], pB):
                d = np.linalg.norm(ps[i]-pB)
                nbs[i][iB] = d
                nbs[iB][i] = d

    if False:
        for p, r in zip(PC, RC):
            t = np.linspace(0, 2.0*np.pi)
            plt.plot(p[0]+r*np.cos(t), p[1]+r*np.sin(t), 'r')
        for i in range(ND*ND+2):
            for j in nbs[i]:
                plt.plot([ps[i][0], ps[j][0]], [ps[i][1], ps[j][1]], 'k')
        plt.axis("equal")
        plt.show()
        __import__('sys').exit(0)

    return ps, nbs, iA, iB


def dijkstra(ps, nbs, iA, iB):

    vals = -np.ones(len(ps))
    vals[iA] = 0
    checked = [iA]
    s0, s1 = 0, len(checked)
    while s0 < s1:
        for i in checked[s0:s1]:
            for i1, w in nbs[i].items():
                if vals[i1] < 0:
                    checked.append(i1)
                if vals[i] + w < vals[i1] or vals[i1] < 0:
                    vals[i1] = vals[i] + w
        s0, s1 = s1, len(checked)

    path = [iB]
    while path[-1] != iA:
        i = path[-1]
        closest = -1
        closestD = INF
        for i1, w in nbs[i].items():
            if i1 in path:
                continue
            err = abs(vals[i]-vals[i1]-w)
            if err < closestD:
                closest = i1
                closestD = err
        path.append(closest)

    pathx = []
    pathy = []
    for i in path[::-1]:
        pathx.append(ps[i][0])
        pathy.append(ps[i][1])
    return np.array(pathx), np.array(pathy)


def optimizePath(PC, RC, pathx, pathy, verbose=True):
    
    def cost(x):
        """cost function and its gradient"""
        def sg(x1, x2):
            dx = x2-x1
            s = np.linalg.norm(dx)
            return s, -dx/s, dx/s
        x = x.reshape(2, len(x)//2).T
        grad = 0.0*x
        s = 0
        for i in range(1, len(x)):
            ds, gi0, gi = sg(x[i-1], x[i])
            s, grad[i-1], grad[i] = s+ds, grad[i-1]+gi0, grad[i]+gi
        ds, gi0, gi = sg([pathx[0],pathy[0]], x[0])
        s, grad[0] = s+ds, grad[0]+gi
        ds, gi0, gi = sg([pathx[-1],pathy[-1]], x[-1])
        s, grad[-1] = s+ds, grad[-1]+gi
        return s, 1.0*grad.T.reshape(len(x)*2)

    def segmentSDF(a, b, p, r):
        pa = p - a
        ba = b - a
        h = np.dot(pa, ba) / np.dot(ba, ba)
        h = max(min(1.0, h), 0.0)
        return np.linalg.norm(pa-ba*h)-r

    def constraint(x):
        """constraint function"""
        x = x.reshape(2, len(x)//2).T
        d = INF
        for p, r in zip(PC, RC):
            for i in range(1, len(x)):
                d = min(d, segmentSDF(x[i-1], x[i], p, r))
            d = min(d, segmentSDF([pathx[0],pathy[0]], x[0], p, r))
            d = min(d, segmentSDF([pathx[-1],pathy[-1]], x[-1], p, r))
        return d

    def segmentSDFg(a, b, p, r):
        pa = (p-a).reshape((2, 1))
        ba = (b-a).reshape((2, 1))
        p = p.reshape((2, 1))
        pb = pa.T @ ba
        bb = ba.T @ ba
        h = pb / bb
        h = max(min(1.0, h), 0.0)
        if h == 0.0 or h == 1.0:
            dhdpa = 0.0*pa.T
            dhdba = 0.0*ba.T
        else:
            dhdpa = ba.T / bb
            dhdba = (bb*pa.T-2*pb*ba.T)/(bb*bb)
        d = pa-ba*h
        dddpa = np.eye(2) - ba @ dhdpa
        dddba = -np.eye(2) * h - ba @ dhdba
        dn = np.linalg.norm(d)
        v = dn - r
        dvdpa = (d.T @ dddpa) / (dn)
        dvdba = (d.T @ dddba) / (dn)
        return v, (-dvdpa-dvdba).reshape(2), dvdba.reshape(2)

    def constraintg(x):
        """constraint function and its gradient"""
        x = x.reshape(2, len(x)//2).T
        d, i0, i1, g0, g1 = INF, -1, -1, None, None
        for p, r in zip(PC, RC):
            for i in range(1, len(x)):
                ds, gi0, gi = segmentSDFg(x[i-1], x[i], p, r)
                if ds < d:
                    d, i0, i1, g0, g1 = ds, i-1, i, gi0, gi
            ds, gi0, gi = segmentSDFg([pathx[0],pathy[0]], x[0], p, r)
            if ds < d:
                d, i0, i1, g0, g1 = ds, -1, 0, gi0, gi
            ds, gi0, gi = segmentSDFg([pathx[-1],pathy[-1]], x[-1], p, r)
            if ds < d:
                d, i0, i1, g0, g1 = ds, -1, len(x)-1, gi0, gi
        grad = 0.0*x
        if i0 != -1:
            grad[i0] = g0
        if i1 != -1:
            grad[i1] = g1
        return grad.T.reshape(len(x)*2)

    constraints = [scipy.optimize.NonlinearConstraint(
        constraint, 0, INF, jac=constraintg)]

    path = np.concatenate((pathx[1:-1], pathy[1:-1]))
    path = scipy.optimize.minimize(cost, path, jac=True, constraints=constraints,
                                   method="SLSQP", options={'maxiter':200})
    if verbose:
        print(path)
    if path.success or False:
        pathx[1:-1] = path.x[:len(pathx)-2]
        pathy[1:-1] = path.x[len(pathx)-2:]
    return path.success, path.nit, pathx, pathy


def plotPath(PC, RC, pathx, pathy, success, time_delta):

    if not success:
        plt.title("FAILED to plan optimal path")
    else:
        plt.title("Path planned in {:.3f}s".format(time_delta))

    for p, r in zip(PC, RC):
        t = np.linspace(0, 2.0*np.pi)
        plt.plot(p[0]+r*np.cos(t), p[1]+r*np.sin(t), 'r')
    plt.plot([0, 1], [0, 1], "ko")

    plt.plot(pathx, pathy, 'k-')
    plt.plot(pathx, pathy, 'k.')

    plt.axis('equal')
    plt.show()


if __name__ == "__main__":

    def testCase(seed, verbose):
        PC, RC = generateRandomCircles(15, seed)
        time0 = perf_counter()
        ps, nbs, iA, iB = generateGraph(PC, RC)
        time1 = perf_counter()
        pathx, pathy = dijkstra(ps, nbs, iA, iB)
        time2 = perf_counter()
        success, niter, pathx, pathy = optimizePath(PC, RC, pathx, pathy, verbose)
        time3 = perf_counter()
        if verbose:
            plotPath(PC, RC, pathx, pathy, success, time3-time0)
        return success, niter, time3-time0, [time1-time0, time2-time1, time3-time2]

    def testCases():
        N = 50
        times = []
        success_count = 0
        for seed in range(N):
            success, niter, tott, steps = testCase(seed, False)
            print(seed, success, niter, tott)
            times.append(steps)
            success_count += success
        times = np.array(times)
        print("{}/{} ({:.2f}±{:.1g}) success".format(
              success_count, N, success_count/N,
              (success_count*(N-success_count)/N**3)**0.5))
        fig, ((ax0, ax1), (ax2, ax3)) = plt.subplots(2, 2)
        ax0.set_title("Total Time (s)")
        ax0.boxplot(np.sum(times, axis=1))
        ax1.set_title("Generate graph")
        ax1.boxplot(times[:, 0])
        ax2.set_title("Planning")
        ax2.boxplot(times[:, 1])
        ax3.set_title("Optimize (s)")
        ax3.boxplot(times[:, 2])
        plt.show()

    testCase(3, True)
    #testCases()
