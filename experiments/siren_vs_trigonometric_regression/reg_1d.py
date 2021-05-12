import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from math import pi, sin, cos, sqrt, hypot
import scipy.sparse.linalg

sz = 256
x = np.linspace(0, 1, sz).reshape((sz, 1))

y = np.exp(np.sin(8*x)) \
    - 0.5*np.exp(np.sin(16*x)) \
    + 0.3*np.exp(np.cos(32*x)) \
    - 0.2*np.exp(np.cos(64*x))

#y = np.sign(x-0.8)-np.sign(x-0.2)+np.abs(x-0.5)+np.abs(x-0.9)


PLOT_GRAPH = True


# neural network, (4+4)+(4×4+4)+(4+1)=33 real numbers

def fit_siren():

    activation = tf.math.sin

    model = tf.keras.Sequential([
        tf.keras.layers.Dense(4, input_dim=1),
        tf.keras.layers.Activation(activation),
        tf.keras.layers.Dense(4, input_dim=1),
        tf.keras.layers.Activation(activation),
        tf.keras.layers.Dense(1),
    ])

    model.compile(
        optimizer=tf.keras.optimizers.SGD(learning_rate=0.03, momentum=0.9),
        loss='mean_squared_error', metrics=['accuracy'])

    losses = []
    
    ITER = 50
    EPOCHS = 100
    
    for i in range(ITER):
        model.fit(x, y, epochs=EPOCHS, verbose=0)

        loss = model.evaluate(x, y, verbose=0)[0]
        print('loss =', loss)
        losses.append(loss)

        if PLOT_GRAPH:
            plt.clf()
            plt.plot(x, y)
            plt.plot(x, model.predict(x))
            plt.savefig(".temp/sn{:02d}.png".format(i+1))

    plt.clf()
    plt.plot([EPOCHS*t for t in range(1,ITER+1)], losses)
    plt.yscale('log')
    plt.savefig(".temp/sn.png")


# trigonometric series regression, 2*deg+1 real numbers


def eval_trig(x, coes):
    deg = (len(coes)-1)//2
    y = coes[0]
    for k in range(1,deg+1):
        y = y + coes[2*k-1]*np.cos(pi*k*x) + coes[2*k]*np.sin(pi*k*x)
    return y


def fit_trig_deg(x, y, deg):
    dim = 2*deg+1

    def generate_u(x):
        u = np.zeros(dim)
        u[0] = 1
        for k in range(1, deg+1):
            u[2*k-1] = np.cos(pi*k*x)
            u[2*k] = np.sin(pi*k*x)
        return u

    cov = np.zeros((dim, dim))
    vec = np.zeros((dim))
    for i in range(len(x)):
        ui = generate_u(x[i])
        cov += np.tensordot(ui, ui, axes=0)
        vec += y[i] * ui

    #coes = np.linalg.solve(cov, vec)
    coes = scipy.sparse.linalg.cg(cov, vec)[0]

    y1 = eval_trig(x, coes)
    loss = np.average((y1-y)**2)
    print('deg =', deg, 'loss =', loss)

    if PLOT_GRAPH:
        plt.clf()
        plt.plot(x, y)
        plt.plot(x, y1)
        plt.savefig(".temp/tr{:02d}.png".format(deg))

    return (coes, loss)


def fit_trig():
    max_deg = 50

    all_coes = []
    losses = []
    for deg in range(1, max_deg+1):
        coes, loss = fit_trig_deg(x, y, deg)
        amps = []
        for k in range(deg):
            amps.append(abs(coes[0]) if k==0 else hypot(coes[2*k-1],coes[2*k]))
        while len(amps)<=max_deg: amps.append(0)
        all_coes.append(amps[:])
        losses.append(loss)

    plt.clf()
    fig, axes = plt.subplots(nrows=2)
    axes[0].pcolormesh(all_coes)
    axes[1].set_yscale('log')
    axes[1].plot(range(1,max_deg+1), losses)
    #plt.show()
    plt.savefig(".temp/tr.png")



# cosine only trigonometric series regression, deg real numbers


def eval_cosine(x, coes):
    y = 0
    for k in range(len(coes)):
        y = y + coes[k]*np.cos(pi*k*x)
    return y


def fit_cosine_deg(x, y, deg):

    cov = np.zeros((deg, deg))
    vec = np.zeros((deg))
    for i in range(len(x)):
        ui = [cos(pi*k*x[i]) for k in range(deg)]
        cov += np.tensordot(ui, ui, axes=0)
        vec += y[i] * ui

    coes = scipy.sparse.linalg.cg(cov, vec)[0]

    y1 = eval_cosine(x, coes)
    loss = np.average((y1-y)**2)
    print('deg =', deg, 'loss =', loss)

    if PLOT_GRAPH:
        plt.clf()
        plt.plot(x, y)
        plt.plot(x, y1)
        plt.savefig(".temp/cr{:02d}.png".format(deg))

    return (coes, loss)


def fit_cosine():
    max_deg = 50

    all_coes = []
    losses = []
    for deg in range(1, max_deg+1):
        coes, loss = fit_cosine_deg(x, y, deg)
        coes = [abs(t) for t in coes]
        while len(coes)<max_deg: coes.append(0)
        all_coes.append(coes[:])
        losses.append(loss)

    plt.clf()
    fig, axes = plt.subplots(nrows=2)
    axes[0].pcolormesh(all_coes)
    axes[1].set_yscale('log')
    axes[1].plot(range(1,max_deg+1), losses)
    #plt.show()
    plt.savefig(".temp/cr.png")



fit_siren()

fit_trig()
fit_cosine()
