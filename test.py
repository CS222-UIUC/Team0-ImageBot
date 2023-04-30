import math
import os
import shutil
from PIL import Image
import cv2
import numpy as np
from scipy.interpolate import griddata
from discord.ext.commands import BadArgument
import matplotlib.pyplot as plt


def voronoi_image(in_path, out_path, num_points: int, seed: int):
    if num_points < 4:
        raise BadArgument("Points must be in range [4, x]")

    np.random.seed(seed)
    img = Image.open(in_path)
    
    np_img = np.array(img)

    height = np_img.shape[0]
    width = np_img.shape[1]

    points = np.random.rand(num_points, 2) * [width, height]

    rgb = np.zeros((num_points, 3), dtype=np.uint8)
    for i in range(num_points):
        p = points[i]
        x, y = int(p[0]), int(p[1])
        rgb[i, :] = np_img[x, y, :3]

    grid_x, grid_y = np.mgrid[0:width, 0:height]
    labels = griddata(points, np.arange(num_points), (grid_x, grid_y), method='nearest')
    rgb_labels = rgb[labels]
    plt.imsave(out_path, rgb_labels)
    


voronoi_image("imgs/duck.png", "imgs/duck1.png", 1000, 0)