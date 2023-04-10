import math
import os
import shutil
from PIL import Image

from discord.ext.commands import BadArgument
from triangler import *

from command import Command
import image_utils

MIN_POINTS = 1
MAX_POINTS = 16383

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
        
        await triangulate_image(img_path, img_path, points=points)
        return img_path

class TriAnimation(Command):
    def __init__(self):
        super().__init__("$triangulate_animate [image link/uploaded image")
    
    async def command(self, img_path):
        #setup output directory
        img_dir = os.path.dirname(img_path)
        out_dir = os.path.join(img_dir, "temp")
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

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
