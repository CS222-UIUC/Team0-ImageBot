import math
import os
import shutil
from PIL import Image
import cv2
import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt

from discord.ext.commands import BadArgument
from triangler import *

from command import Command
import image_utils

MIN_POINTS = 1
MAX_POINTS = 16383

def normalize_image(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    img = cv2.normalize(img, None, 255, 0, cv2.NORM_MINMAX, cv2.CV_8U)
    cv2.imwrite(img_path, img)

async def triangulate_image(in_path, out_path, points: int):
    if points > MAX_POINTS or points < MIN_POINTS:
        raise BadArgument(f"Number of points must be in range [{MIN_POINTS}, {MAX_POINTS}]")
    triangler_instance = Triangler(
        edge_method=EdgeMethod.SOBEL,
        sample_method=SampleMethod.POISSON_DISK,
        color_method=ColorMethod.CENTROID,
        points=points,
        blur=2,
        pyramid_reduce=True,
    )
    triangler_instance.convert_and_save(in_path, out_path)

class Triangulate(Command):
    def __init__(self):
        super().__init__("$triangulate [points] [image link/uploaded image]")
    
    async def command(self, img_path, points):
        try:
            points = int(points)
        except ValueError:
            image_utils.delete_file(img_path)
            raise BadArgument
        normalize_image(img_path)
        await triangulate_image(img_path, img_path, points=points)
        return img_path

class TriAnimation(Command):
    def __init__(self):
        super().__init__("$triangulate_animate [image link/uploaded image]")
    
    async def command(self, img_path):
        #setup output directory
        img_dir = os.path.dirname(img_path)
        out_dir = os.path.join(img_dir, "temp")
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

        normalize_image(img_path)

        def f(p, L, k, p0, y0):
            return L/(1+math.exp(-k*(p-p0))) - y0

        img_name = os.path.splitext(os.path.basename(img_path))
        base_name = img_name[0]
        extension = img_name[1]

        #create frames
        frames = []
        num_frames = 25
        for p in range(1, num_frames + 1): 
            out_path = os.path.join(out_dir, f"{base_name}_{p:02d}.{extension}")           
            await triangulate_image(img_path, out_path, f(p, 5000, 0.4, 14, 18))
            frames.append(Image.open(out_path))
        
        for p in range(num_frames, 1, -1):
            #copy old frames
            i = 2 * num_frames - p + 1
            frame_p = os.path.join(out_dir, f"{base_name}_{p:02d}.{extension}")
            frame_i = os.path.join(out_dir, f"{base_name}_{i:02d}.{extension}")
            shutil.copy(frame_p, frame_i)
            frames.append(Image.open(frame_i))
        
        #create gif
        output_file = os.path.join(img_dir, "output.gif")
        frames[0].save(output_file, save_all=True, append_images=frames[1:], duration=100, loop=0)

        #delete output dir
        shutil.rmtree(out_dir)
        return output_file

async def voronoi_image(in_path, out_path, num_points: int, seed: int):
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

