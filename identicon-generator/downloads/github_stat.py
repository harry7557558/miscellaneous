import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import colorsys

# load images
dirname = "github/"
filenames = [dirname+filename for filename in os.listdir(dirname)]
imgs = [np.array(Image.open(filename)) for filename in filenames[:]]

# convert to 5x5 color array
for i in range(len(imgs)):
    imgs[i] = imgs[i][35:385,35:385,:]
    imgs[i] = imgs[i].reshape(5, 70, 5, 70, 3).max(3).max(1)

# visualize color distribution
def visualize_color_rgb(imgs):
    cols = np.array([np.amin(img, (0,1)) for img in imgs])
    plt.clf()
    ax = plt.figure().add_subplot(projection='3d', proj_type='ortho')
    ax.scatter(cols[:, 0], cols[:, 1], cols[:, 2], c=cols/255.0)
    plt.show()

def visualize_color_hls(imgs):
    rgb = np.array([np.amin(img, (0,1)) for img in imgs])
    hls = np.array([colorsys.rgb_to_hls(*(col/255.0)) for col in rgb])
    plt.clf()
    ax = plt.figure().add_subplot(projection='3d', proj_type='ortho')
    ax.scatter(hls[:, 0], hls[:, 1], hls[:, 2], c=rgb/255.0)
    plt.show()

visualize_color_hls(imgs)
