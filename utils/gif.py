from PIL import Image, ImageSequence
from discord.ext.commands import BadArgument
import os

from command import Command
import image_utils

DEFAULT_GIF_PATH = "imgs\default.gif"
APP_IMGS_DIR = "imgs/app_imgs"

def clear_all_images():
    for filename in os.listdir(APP_IMGS_DIR):
        os.remove(os.path.join(APP_IMGS_DIR, filename))

def are_image_paths_valid(image_paths):
    image_paths = image_paths.split()
    is_valid = True
    index = 0
    if not os.path.exists(APP_IMGS_DIR):
        os.mkdir(APP_IMGS_DIR)
    for i in range(0, len(image_paths)):
        try:
            image_paths[i] = image_utils.download_img(image_paths[i], APP_IMGS_DIR)
            filename, ext = os.path.splitext(image_paths[i])
            new_image_path = f"{filename}{i}{ext}"
            os.rename(image_paths[i], new_image_path)
            image_paths[i] = new_image_path
        except BadArgument:
            index = i
            is_valid = False
            break
    if not is_valid:
        for i in range(0, index):
            image_utils.delete_img(image_paths[i])
    return (is_valid, image_paths)

class GifCreate(Command):
    def __init__(self):
        super().__init__("$create_gif [\"image_url1 image_url2 ... image_urln\"] [cover_image_url]\nMake sure all urls are valid and image urls are separated by spaces and in double quotation")

    async def command(self, cover_image_path, image_paths):
        is_valid, image_paths = are_image_paths_valid(image_paths)
        if not is_valid or len(image_paths) == 0:
            raise BadArgument
        im = Image.open(cover_image_path)
        width, height = im.width, im.height
        images = [im]
        for i in range(0, len(image_paths)):
            img_path = image_paths[i]
            img = Image.open(img_path)
            img = img.resize((width, height))
            images.append(img)
            img.save(img_path)
        im.save(DEFAULT_GIF_PATH, save_all=True, append_images=images, duration=500, loop=0)
        clear_all_images()
        return DEFAULT_GIF_PATH

class GifAppend(Command):
    def __init__(self):
        super().__init__("$append_gif [\"image_url1 image_url2 ... image_urln\"] [gif_url]\nMake sure all urls are valid and image urls are separated by spaces and in double quotation")
    
    async def command(self, gif_path, image_paths):
        is_valid, image_paths = are_image_paths_valid(image_paths)
        if not is_valid:
            raise BadArgument
        im = Image.open(gif_path)
        width, height = im.width, im.height
        images = [frame.copy() for frame in ImageSequence.Iterator(im)]
        for i in range(0, len(image_paths)):
            img_path = image_paths[i]
            img = Image.open(img_path)
            if img.format == 'GIF':
                for j in range(0, img.n_frames):
                    img.seek(j)
                    frame = img.resize((width, height))
                    images.append(frame)
                img.close()
            else:
                img = img.resize((width, height))
                images.append(img)
                img.save(img_path)
        images[0].save(gif_path, save_all=True, append_images=images[1:], duration=500, loop=0)
        clear_all_images()
        return gif_path