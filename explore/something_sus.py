import numpy as np
import scipy.stats
import matplotlib.pyplot as plt

# (description, time spent in h, mark get)
DATA = [
[
    "grade 9",
    ("ESLDO drawing", 2, 37/40),
    ("ESLDO presentation 1", 10, 38/40),
    ("ESLDO presentation 2", 5, 39/40),
    ("ESLDO essay", 8, 38/40),
    ("AVI1O box drawing", 2, 90/100),
    ("AVI1O story", 6, 39/40),
    ("AVI1O printmaking", 8, 39/40),
    ("AVI1O CPT", 80, 57/60),
    ("HRT3M CPT", 8, 38/40),
],
[
    "grade 10",
    ("ESLEO intro", 6, 38/40),
    ("ESLEO presentation", 10, 37/40),
    ("ESLEO CPT", 50, 38/40),
    ("HRE2O CPT", 10, 40/40),
    ("ENG2D CPT", 30, 85/100),
    ("GLC2O intro", 3, 39/40),
    ("CHC2D final", 6, 39/40),
    ("CHV2O presentation", 5, 39/40),
    ("ASM2O intro", 4, 38/40),
    ("ASM2O CPT", 20, 95/100),
    ("ASM2O animation", 10, 40/40),
    ("ASM2O research", 10, 40/40),
],
[
    "grade 11",
    ("SPH3U CPT", 20, 40/40),
    ("AVI3M practice", 1, 85/100),
    ("AVI3M intro", 10, 40/40),
    ("AVI3M drawing 1", 8, 38/40),
    ("AVI3M drawing 2", 6, 37/40),
    ("AVI3M CPT", 15, 39/40),
    ("HRT3M CPT", 12, 39/40),
    ("SCH3U CPT", 20, 90/100),
    ("ICS3U CPT", 6, 100/100),
    ("ENG3U intro", 6, 90/100),
    ("ENG3U presentation", 10, 38/40),
    ("ENG3U CPT", 10, 37.5/40),
    ("ENG3U essay", 20, 29.5/40),
],
[
    "grade 12",
    ("AVI4M sketchbook", 8, 90/100),
    ("AVI4M wearable art", 10, 38/40),
    ("AVI4M research 1", 5, 39/40),
    ("AVI4M research 2", 4, 38.5/40),
    ("AVI4M CPT", 70, 99/100),
    ("HRE4M CPT", 4, 20/20),
    ("ICS4U CPT", 4, 40/40),
    ("SCH4U research", 10, 10/10),
    ("MDM4U CPT", 12, 68.5/70),
    ("ENG4U essay 1", 10, 36/40),
    ("ENG4U essay 2", 8, 36/40),
    ("ENG4U presentation 1", 10, 38/40),
    ("ENG4U presentation 2", 20, 36.5/40),
    ("ENG4U essay 3", 8, 39/40),
    ("ENG4U essay 4", 7, 37.5/40),
    ("ENG4U CPT", 6, 40/40),
],
[
    "first year",
    ("PHY180 lab 1", 20, 30/30),
    ("PHY180 lab 2", 10, 30/30),
    ("PHY180 lab 3", 2, 35/36),
    #("ESC101 fsa", 6, 13/20),
    #("ESC101 dsa", 5, 13.5/20),
    ("ESC180 project 1", 1.5, 111/120),
    ("ESC180 project 2", 3, 83.5/88.5),
    ("ESC180 project 3", 2, 90/90),
    ("an average CIV102 assignment", 5, 4/5),
    ("CIV102 bridge 1", 15, 6/7),
]
][:]


def plot_grade_time():
    Xs, Ys = [], []
    for data in DATA:
        label, data = data[0], data[1:]
        X = [d[1] for d in data]
        Y = [100*d[2] for d in data]
        plt.plot(X, Y, 'o' if 'grade' in label else 's', label=label)
        Xs, Ys = Xs+X, Ys+Y

    res = scipy.stats.linregress(Xs, Ys)
    m, b = res.slope, res.intercept
    x = np.linspace(0, plt.gca().get_xlim()[1])
    plt.plot(x, m*x+b, "--",
             label="line of best fit\nr²={:.2g}".format(res.rvalue**2))

    plt.title("Grade on assignments vs. Productive time spent")
    plt.xlabel("Time (hours)")
    plt.ylabel("Grade (%)")
    plt.legend()
    plt.show()


def plot_time_dist():
    Xs = sum([[d[1] for d in data[1:]] for data in DATA], [])
    plt.hist(Xs, bins=10, density=True)

    mean = np.mean(Xs)
    var = np.var(Xs)
    print("mean =", mean)
    print("stdev =", var**0.5)
    l = 1.0/var**0.5
    x = np.linspace(0, plt.gca().get_xlim()[1])
    plt.plot(x, l*np.exp(-l*x), '--')

    plt.title("Distribution of time (in hours) spent on assignments")
    plt.show()


def plot_grade_dist():
    Xs = sum([[1.0-d[2] for d in data[1:]] for data in DATA], [])
    plt.hist(Xs, bins=10, density=True)

    mean = np.mean(Xs)
    var = np.var(Xs)
    print("mean =", mean)
    print("stdev =", var**0.5)
    x = np.linspace(0, plt.gca().get_xlim()[1])

    # exponential distribution
    l = 1.0/var**0.5
    plt.plot(x, l*np.exp(-l*x),
             '--', label="exponential fit")

    # normal distribution
    plt.plot(x, np.exp(-0.5*(x-mean)**2/var)/np.sqrt(2*np.pi*var),
             '--', label="normal fit")

    plt.title("Distribution of assignment grades")
    plt.legend()
    plt.show()


def plot_grade_time_dist():
    Xs = sum([[d[1] for d in data[1:]] for data in DATA], [])
    Ys = sum([[100*d[2] for d in data[1:]] for data in DATA], [])
    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.plot(Xs, Ys, 'o')
    # assume two variables are independent
    u = scipy.stats.qmc.Halton(d=2, seed=80).random(n=len(Xs))
    l1 = np.var(Xs)**-0.5
    l2 = np.var(Ys)**-0.5
    x1 = -np.log(1.0-u[:,0])/l1
    y1 = 100+np.log(1.0-u[:,1])/l2
    ax2.plot(x1, y1, 'o')
    ax1.set_title("Grade-Time data")
    ax2.set_title("Fit to distribution")
    plt.show()


if __name__ == "__main__":
    plot_grade_time()
    #plot_time_dist()
    #plot_grade_dist()
    #plot_grade_time_dist()
