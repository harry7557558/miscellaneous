from typing import List, Tuple

import numpy as np
from PIL import Image

import scipy.spatial


def load_font(filename: str) -> List[np.array]:
    """Load GNU Unifont plane as a list of 16x16 numpy arrays"""
    image = Image.open(filename)
    pixels = np.asarray(image).astype(np.float32)
    pixels = pixels[64:, 32:]
    assert pixels.shape == (4096, 4096)

    font = []
    for code in range(65536):
        row = 16*(code//256)
        col = 16*(code%256)
        subimg = pixels[row:row+16, col:col+16]
        font.append(1.0-subimg)

    return font


def write_image(data: np.array, filename: str):
    """Save a font bitmap for debugging purpose"""
    data = data.astype(bool)
    image = Image.fromarray(data)
    image.save(filename)


def image_distance(img1: np.array, img2: np.array) -> float:
    """Calculate the distance between two images for comparism"""
    assert img1.shape == img2.shape
    img1 = img1.flatten()
    img2 = img2.flatten()
    # return scipy.spatial.distance.euclidean(img1, img2)
    # return scipy.spatial.distance.cosine(img1, img2)
    return scipy.spatial.distance.cityblock(img1, img2)


def closest_chars(code: int, font: List[np.array]) -> List[Tuple[int, float]]:
    """Find most similar fonts to the given character code in the font list,
        Returns a sorted list of character code and distances """
    img = font[code]
    dists = []
    for c in range(len(font)):
        if c == code:
            continue
        dist = image_distance(img, font[c])
        dists.append((c, dist))
    dists = sorted(dists, key=lambda x: x[1])
    return dists


def print_similar(c: str, count: int):
    """Print similar characters"""
    print(c, end=' ')
    dists = closest_chars(ord(c), font)
    for i in range(count):
        print(chr(dists[i][0]), end='')
    print(end='\n')


if __name__ == "__main__":
    font = load_font("unifont-14.0.01.bmp")

    print_similar('A', 99)
    print_similar('囧', 99)
    print_similar('물', 99)
    print_similar('☺', 99)
    print_similar('−', 99)
