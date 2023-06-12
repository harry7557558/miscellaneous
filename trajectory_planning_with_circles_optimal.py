import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize
from math import gcd
from time import perf_counter


pA = np.array([0, 0])
pB = np.array([1, 1])
INF = 10.0


def generateRandomCircles(nc, seed):
    np.random.seed(seed)
    PC = []
    RC = []
    while len(PC) < nc:
        p = np.random.random(2)
        r = 0.025+abs(np.random.normal(0, 0.05, size=1))[0]
        if np.linalg.norm(p) > r and np.linalg.norm(p-[1,1]) > r:
            PC.append(p)
            RC.append(r)
    return np.array(PC), np.array(RC)


def generateGraph(PC, RC):

    def isOccluded(p0, p1):
        eps = 1e-6
        dp = p1 - p0
        for p, r in zip(PC, RC):
            op = p0 - p
            a = np.dot(dp, dp)
            b = np.dot(op, dp)
            c = np.dot(op, op) - r*r
            if c < -eps:
                return True
            d = b*b-a*c
            if d < 0:
                continue
            if eps <= (-b-d**0.5)/a <= 1-eps:
                return True
            if eps <= (-b+d**0.5)/a <= 1-eps:
                return True
        return False

    def isOccludedArc(p0, p1, c0, r0):
        n = np.array([p1[1]-p0[1], p0[0]-p1[0]])
        d = n[0]*p0[0] + n[1]*p0[1]
        for c1, r1 in zip(PC, RC):
            if (c0 == c1).all():
                continue
            d0 = np.dot(c0, c0) - r0*r0
            d1 = np.dot(c1, c1) - r1*r1
            c = np.linalg.solve([
                [c0[0]-c1[0], c0[1]-c1[1]],
                [c0[1]-c1[1], c1[0]-c0[0]]
            ], [
                0.5*(d0-d1),
                (c0[1]-c1[1])*c0[0]+(c1[0]-c0[0])*c0[1]
            ])
            et = c - c0
            etl = np.linalg.norm(et)
            if etl >= r0:
                continue
            enl = (r0*r0-etl*etl)**0.5
            en = np.array([et[1], -et[0]]) * enl / etl
            a1, a2 = c+en, c-en
            p_ = 0.5*(p0+p1)+0.1*n
            if np.dot(n, a1) > d or np.dot(n, a2) > d:
                return True
        return False

    # between endpoints
    nodes = [pA, pB]
    paths = [{}, {}]
    circle_nodes = [set({}) for _ in range(len(PC))]
    if not isOccluded(pA, pB):
        w = np.linalg.norm(pB-pA)
        paths[0][1] = w
        paths[1][0] = w

    def add_path(c1, c2, p1, p2):
        if isOccluded(p1, p2):
            return
        i1, i2 = len(nodes), len(nodes)+1
        if c1 < 0:
            i1, i2 = -1-c1, i2-1
        else:
            circle_nodes[c1].add(i1)
            nodes.append(p1)
            paths.append({})
        if c2 < 0:
            i1, i2 = i1, -1-c2
        else:
            circle_nodes[c2].add(i2)
            nodes.append(p2)
            paths.append({})
        w = np.linalg.norm(p2-p1)
        paths[i1][i2] = w
        paths[i2][i1] = w

    # between circles
    N = len(PC)
    for i in range(N):
        for j in range(i):
            dp = PC[j] - PC[i]
            dh = np.linalg.norm(dp)
            # same side
            sin_theta = (RC[j]-RC[i]) / dh
            if sin_theta <= -1 or sin_theta >= 1:
                continue
            theta = np.arcsin(sin_theta)
            et = np.sin(theta) * dp/dh
            en = np.cos(theta) * np.array([dp[1],-dp[0]])/dh
            add_path(i, j, PC[i]+RC[i]*(-et+en), PC[j]+RC[j]*(-et+en))
            add_path(i, j, PC[i]+RC[i]*(-et-en), PC[j]+RC[j]*(-et-en))
            # different sides
            sin_theta = (RC[j]+RC[i]) / dh
            if sin_theta <= 0 or sin_theta >= 1:
                continue
            theta = np.arcsin(sin_theta)
            et = np.sin(theta) * dp/dh
            en = np.cos(theta) * np.array([dp[1],-dp[0]])/dh
            add_path(i, j, PC[i]+RC[i]*(et+en), PC[j]+RC[j]*(-et-en))
            add_path(i, j, PC[i]+RC[i]*(et-en), PC[j]+RC[j]*(-et+en))

    # endpoint to circle
    for ie, pe in [(0, pA), (1, pB)]:
        for i in range(N):
            dp = PC[i] - pe
            dh = np.linalg.norm(dp)
            sin_theta = RC[i] / dh
            assert 0 <= sin_theta <= 1 and "endpoint inside circle"
            et = RC[i] * sin_theta * dp/dh
            en = RC[i] * (1-sin_theta**2)**0.5 * np.array([dp[1],-dp[0]])/dh
            add_path(-1-ie, i, pe, PC[i]-et+en)
            add_path(-1-ie, i, pe, PC[i]-et-en)

    # same circles
    for i in range(N):
        p = PC[i]
        ang = lambda j: np.arctan2(nodes[j][1]-p[1],nodes[j][0]-p[0])
        cnodes = sorted(circle_nodes[i], key=ang)
        for j0 in range(len(cnodes)):
            j1 = (j0+1) % len(cnodes)
            j0, j1 = cnodes[j0], cnodes[j1]
            p0, p1 = nodes[j0]-p, nodes[j1]-p
            if isOccludedArc(nodes[j0], nodes[j1], PC[i], RC[i]):
                continue
            w = RC[i] * ((ang(j1)-ang(j0)) % (2.0*np.pi))
            assert w >= 0.0
            paths[j0][j1] = w
            paths[j1][j0] = w

    if False:
        for p, r in zip(PC, RC):
            t = np.linspace(0, 2.0*np.pi)
            plt.plot(p[0]+r*np.cos(t), p[1]+r*np.sin(t), 'r')
        for i in range(len(paths)):
            for j in paths[i]:
                assert i in paths[j]
                plt.plot([nodes[i][0], nodes[j][0]],
                         [nodes[i][1], nodes[j][1]], 'k-')
        plt.axis("equal")
        plt.show()
        __import__('sys').exit(0)

    return np.array(nodes), paths, 0, 1


def dijkstra(ps, nbs, iA, iB):

    vals = INF * np.ones(len(ps))
    vals[iA] = 0
    checked = [iA]
    s0, s1 = 0, len(checked)
    while s0 < s1:
        for i in checked[s0:s1]:
            for i1, w in nbs[i].items():
                if vals[i] + w < vals[i1]:
                    vals[i1] = vals[i] + w
                    checked.append(i1)
        s0, s1 = s1, len(checked)

    #plt.scatter(ps[:, 0], ps[:, 1], c=vals)
    #plt.axis('equal')
    #plt.show()

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

    return path[::-1]


def plotPath(PC, RC, nodes, paths, path, time_delta):

    plt.title("Path planned in {:.3f}s".format(time_delta))

    for p, r in zip(PC, RC):
        t = np.linspace(0, 2.0*np.pi)
        plt.plot(p[0]+r*np.cos(t), p[1]+r*np.sin(t), 'r')
    plt.plot([0, 1], [0, 1], "ko")

    ipoints = nodes[path]
    plt.plot(ipoints[:, 0], ipoints[:, 1], 'k.')

    et = None
    for i1, i2 in zip(path[:-1], path[1:]):
        p1, p2 = nodes[i1], nodes[i2]
        d, w = np.linalg.norm(p2-p1), paths[i1][i2]
        assert d <= w
        if d > 0.9999*w:
            plt.plot([p1[0], p2[0]], [p1[1], p2[1]], 'k-')
        else:
            a = d/w
            I = lambda x: ((a+np.cos(x))*x-2*np.sin(x))*x/(np.cos(x)*x-np.sin(x))
            theta = I(I(I(I(2*np.arccos(a)))))
            r = w / (2.0*theta)
            d = (p2-p1) / np.linalg.norm(p2-p1)
            n = np.array([-d[1], d[0]])
            if np.dot(et, n) > 0.0:
                n = -n
            c = 0.5*(p1+p2) + r*np.cos(theta) * n
            u = (p1 - c).reshape((2, 1))
            v = np.array([[-u[1][0]], [u[0][0]]])
            if np.dot(et, v) < 0.0:
                v = -v
            t = np.linspace(0, 2*theta, 20).reshape((1, 20))
            ps = c.reshape((2, 1)) + u@np.cos(t) + v@np.sin(t)
            plt.plot(ps[0], ps[1], 'k-')
            
        et = p2-p1

    plt.axis('equal')
    plt.show()


if __name__ == "__main__":

    def testCase(seed, verbose):
        PC, RC = generateRandomCircles(15, seed)
        time0 = perf_counter()
        nodes, paths, iA, iB = generateGraph(PC, RC)
        time1 = perf_counter()
        path = dijkstra(nodes, paths, iA, iB)
        time2 = perf_counter()
        if verbose:
            plotPath(PC, RC, nodes, paths, path, time2-time0)
        return time2-time0, [time1-time0, time2-time1]

    def testCases():
        N = 200
        times = []
        for seed in range(N):
            tott, steps = testCase(seed, False)
            print(seed, tott)
            times.append(steps)
        times = np.array(times)
        fig, (ax0, ax1, ax2) = plt.subplots(1, 3)
        ax0.set_title("Total Time (s)")
        ax0.boxplot(np.sum(times, axis=1))
        ax1.set_title("Generate graph")
        ax1.boxplot(times[:, 0])
        ax2.set_title("Planning")
        ax2.boxplot(times[:, 1])
        plt.show()

    testCase(3, True)
    #testCases()
