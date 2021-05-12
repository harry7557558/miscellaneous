import numpy as np
from math import pi, sin, cos, sqrt, hypot
from matplotlib import image
import matplotlib.pyplot as plt
import scipy.sparse.linalg

# shape=(256,256), dtype=float
image = image.imread('cameraman.png').min(2)


x = np.zeros((256*256,2))
for i in range(256*256):
    x[i][0] = (i//256)/255
    x[i][1] = (i%256)/255

y = image.reshape(256*256)


def fit_cosine(x, y, deg):
    dim = deg*deg

    def generate_u(x):
        ui = np.array([cos(pi*i*x[0]) for i in range(deg)])
        uj = np.array([cos(pi*j*x[1]) for j in range(deg)])
        return np.tensordot(ui, uj, axes=0).reshape((deg*deg))

    cov = np.zeros((dim, dim))
    vec = np.zeros((dim))

    for i in range(len(x)):
        ui = generate_u(x[i])
        cov += np.tensordot(ui, ui, axes=0)
        vec += y[i] * ui

    coes = scipy.sparse.linalg.cg(cov, vec)[0]
    coes = coes.reshape((deg, deg))

    y1 = np.zeros((len(y)))
    for i in range(deg):
        for j in range(deg):
            y1 += coes[i][j] * np.cos(pi*i*x[:,0]) * np.cos(pi*j*x[:,1])

    loss = np.average((y-y1)**2)
    print(loss)
    
    plt.clf()
    fig, axes = plt.subplots(ncols=2)
    axes[0].imshow(y.reshape((256,256)), cmap=plt.get_cmap('gray'))
    axes[1].imshow(y1.reshape((256,256)), cmap=plt.get_cmap('gray'))
    plt.savefig('.temp/reg_2d_cosine.png')


# 256 real numbers
fit_cosine(x, y, 16)
