from PIL import ImageOps, Image, ImageFilter, ImageSequence
from discord.ext.commands import BadArgument
from discord.ext.commands import UserInputError
from fractions import Fraction
import os

from command import Command
import image_utils

FILE_SIZE_LIMIT = 1 << 26 # 64 MB
DISPLAY_FILE_SIZE_LIMIT = 1 << 23 # 8 MB
DEFAULT_GIF_PATH = "imgs\default.gif"
DEFAULT_QUALITY = 75
FILE_SIZE_UNITS = {0 : 'B', 1 : 'KB', 2 : 'MB'}
APP_IMGS_DIR = "imgs/app_imgs"

def get_file_units(size_in_bytes):
    size = float(size_in_bytes)
    unit = 0
    while True:
        size_in_bytes = size_in_bytes >> 10
        if size_in_bytes == 0:
            break
        unit += 1
    size = f'{round(size / (1 << (unit * 10)), 2)} {FILE_SIZE_UNITS[unit]}'
    return size

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

class ImageScaling(Command):
    def __init__(self):
        super().__init__("$scale [factor] [image link/uploaded image]")
    
    async def command(self, img_path, factor, cntx):
        display = await self.image_scaling(img_path, factor)
        if not display:
            await cntx.send("To see the image, please copy the link and open it in a browser")
        return img_path

    async def image_scaling(self, img_path, factor):
        try:
            factor = float(Fraction(factor))
        except ValueError:
            image_utils.delete_file(img_path)
            raise BadArgument
        if factor <= 0:
            image_utils.delete_file(img_path)
            raise BadArgument
        size = os.stat(img_path).st_size
        new_size = size
        if factor > 1:
            new_size = size * factor**2
            if new_size > FILE_SIZE_LIMIT:
                image_utils.delete_file(img_path)
                raise UserInputError
        display = True
        if new_size > DISPLAY_FILE_SIZE_LIMIT:
            display = False
        im = Image.open(img_path)
        try:
            output = ImageOps.scale(im, factor)
        except ValueError:
            im.close()
            image_utils.delete_file(img_path)
            raise UserInputError
        output.save(img_path)
        return display

class ImageResizing(Command):
    def __init__(self):
        super().__init__("$resize [width] [height] [image link/uploaded image].\n\t-Width and height are in pixels")
    
    async def command(self, img_path, width, height, cntx):
        display = await self.image_resizing(img_path, width, height)
        if not display:
            await cntx.send("To see the image, please copy the link and open it in a browser")
        return img_path

    async def image_resizing(self, image, width, height):
        try:
            width = int(width)
            height = int(height)
        except ValueError:
            image_utils.delete_file(image)
            raise BadArgument
        if width <= 0 or height <= 0 or width > 65500 or height > 65500:
            image_utils.delete_file(image)
            raise BadArgument
        im = Image.open(image)
        old_width = im.width
        old_height = im.height
        size = os.stat(image).st_size
        new_size = size
        if width > old_width or height > old_height:
            factor = width * height / (old_width * old_height)
            new_size = size * factor
            if new_size > FILE_SIZE_LIMIT:
                im.close()
                image_utils.delete_file(image)
                raise UserInputError
        display = True
        if new_size > DISPLAY_FILE_SIZE_LIMIT:
            display = False
        output = im.resize((width, height))
        output.save(image)
        return display
        
class ImageRotation(Command):
    def __init__(self):
        super().__init__("$rotate [degree] [image link/uploaded image].\n\t-degree: number specifying number of degrees counterclockwise to rotate")

    async def command(self, img_path, degree):
        try:
            degree = float(degree)
        except ValueError:
            image_utils.delete_file(img_path)
            raise BadArgument
        degree = degree % 360
        im = Image.open(img_path)
        output = im.rotate(degree,expand=True)
        output.save(img_path)
        return img_path

class ImageFlip(Command):
    def __init__(self):
        super().__init__("$flip [direction] [image link/uploaded image].\n\t-direction: 0 flips left to right, 1 flips up to down")

    async def command(self, img_path, direction):
        try:
            direction = int(direction)
        except ValueError:
            image_utils.delete_file(img_path)
            raise BadArgument
        if direction != 0 and direction != 1:
            image_utils.delete_file(img_path)
            raise BadArgument
        im = Image.open(img_path)
        output = im.transpose(direction)
        output.save(img_path)
        return img_path

class EdgeDetect(Command):
    def __init__(self):
        super().__init__("$edge_detect [image link/uploaded image]")
        
    async def command(self, img_path):
        im = Image.open(img_path)
        im = im.convert("L")
        output = im.filter(ImageFilter.Kernel((5,5), (1, 1, 1, 1, 1,
                                                    1, 1, 1, 1, 1,
                                                    1, 1, -24, 1, 1,
                                                    1, 1, 1, 1, 1,
                                                    1, 1, 1, 1, 1), 1, 0))
        output.save(img_path)
        return img_path

class Compress(Command):
    def __init__(self):
        super().__init__("$compress [rate] [url]\n-Rate is a real number between 0 and 1, inclusive")

    async def command(self, img_path, rate, cntx):
        old_file_size, new_file_size, new_file_name = await self.image_compression(img_path, rate)
        await cntx.send(f"Original file size is {old_file_size}, and compressed file size is {new_file_size}")
        return new_file_name

    async def image_compression(self, img_path, rate):
        old_file_size = os.stat(img_path).st_size
        im = Image.open(img_path)
        new_file_name = img_path
        if im.format != 'JPEG':
            im = im.convert('RGB')
            new_file_name = img_path[:-3] + "jpg"
        try:
            rate = float(rate)
        except ValueError:
            im.close()
            image_utils.delete_file(img_path)
            raise BadArgument
        if rate < 0 or rate > 1:
            im.close()
            image_utils.delete_file(img_path)
            raise BadArgument
        if (new_file_name == None):
            qlt = int(rate*DEFAULT_QUALITY)
        else:
            qlt = int(rate*100)

        if (new_file_name == None):
            im.save(img_path, quality=qlt)
            new_file_size = get_file_units(os.stat(img_path).st_size)
        else:
            im.save(new_file_name, quality=qlt)
            new_file_size = get_file_units(os.stat(new_file_name).st_size)
        old_file_size = get_file_units(old_file_size)
        return (old_file_size, new_file_size, new_file_name)

class GifCreate(Command):
    def __init__(self):
        super().__init__("$create_gif [\"image1_url...\"] [cover_image_url]\nMake sure all urls are valid and image urls are separated by spaces and in double quotation")

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
        super().__init__("$append_gif [\"image1_url...\"] [gif_url]\nMake sure all urls are valid and image urls are separated by spaces and in double quotation")
    
    async def command(gif_path, image_paths):
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
