import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# load images
dirname = "gravatar/"
filenames = [dirname+filename for filename in os.listdir(dirname)]
imgs = [np.array(Image.open(filename))[:,:,:3] for filename in filenames[:]]
imgs_bin = []
for img in imgs:
    img = img.min(2)/255.0
    imgs_bin.append((img>0.5*np.amin(img)+0.5).astype(np.int8))


# visualize color distribution
def visualize_color(imgs):
    cols = np.array([np.amin(img, (0,1)) for img in imgs])
    plt.clf()
    ax = plt.figure().add_subplot(projection='3d', proj_type='ortho')
    ax.scatter(cols[:, 0], cols[:, 1], cols[:, 2], c=cols/255.0)
    plt.show()


# check the occurrence of types of block

def is_equal(a0, b0):
    """ consider rotation and flip effects """
    threshold = 0.05*a0.size
    ca = np.count_nonzero(a0) / a0.size
    cb = np.count_nonzero(b0) / b0.size
    if min(abs(ca-cb),
           abs(ca-(1-cb))) > threshold/a0.size:
        return False
    if abs(ca-(1-cb)) < threshold/a0.size:
        b0 = 1-b0
        cb = 1-cb
    a, b = a0, b0  # [[1,0],[0,1]]
    if np.count_nonzero(a!=b) < threshold: return True
    if np.count_nonzero(a!=1-b) < threshold: return True
    a = np.flip(a0, (0))  # [[1,0],[0,-1]]
    if np.count_nonzero(a!=b) < threshold: return True
    if np.count_nonzero(a!=1-b) < threshold: return True
    a = np.flip(a0, (1))  # [[-1,0],[0,1]]
    if np.count_nonzero(a!=b) < threshold: return True
    if np.count_nonzero(a!=1-b) < threshold: return True
    a = np.flip(a0, (0, 1))  # [[-1,0],[0,-1]]
    if np.count_nonzero(a!=b) < threshold: return True
    if np.count_nonzero(a!=1-b) < threshold: return True
    a = np.transpose(a0)  # [[0,1],[1,0]]
    if np.count_nonzero(a!=b) < threshold: return True
    if np.count_nonzero(a!=1-b) < threshold: return True
    a = np.flip(np.transpose(a0), (0))  # [[0,-1],[1,0]]
    if np.count_nonzero(a!=b) < threshold: return True
    if np.count_nonzero(a!=1-b) < threshold: return True
    a = np.flip(np.transpose(a0), (1))  # [[0,1],[-1,0]]
    if np.count_nonzero(a!=b) < threshold: return True
    if np.count_nonzero(a!=1-b) < threshold: return True
    a = np.flip(np.transpose(a0), (0, 1))  # [[0,-1],[-1,0]]
    if np.count_nonzero(a!=b) < threshold: return True
    if np.count_nonzero(a!=1-b) < threshold: return True
    return False

def block_types(imgs):
    types = []
    for img in imgs:
        occurred = False
        for tp in types:
            if is_equal(tp, img):
                occurred = True
                break
        if not occurred:
            types.append(img)
    return types


if __name__ == "__main__":
    imgs_bin = np.array(imgs_bin)
    types = block_types(imgs_bin[:,64:128,64:128])  # 14
    types = block_types(imgs_bin[:,0:64,64:128])  # 45
    types = block_types(imgs_bin[:,0:64,0:64])  # 45
    print(len(types))
    plt.clf()
    figsize = (10, 8)
    fig = plt.figure(figsize=figsize)
    for i in range(0, min(len(types),np.prod(figsize))):
        fig.add_subplot(*figsize, i+1)
        plt.imshow(types[i])
    plt.show()
