from PIL import ImageOps, Image, ImageFilter, ImageSequence
from discord.ext.commands import BadArgument
from discord.ext.commands import UserInputError
from fractions import Fraction
import os

import image_utils

file_size_limit = 1 << 26 # 64 MB
display_file_size_limit = 1 << 23 # 8 MB
default_gif_path = "imgs\default.gif"
default_quality = 75
file_size_units = {0 : 'B', 1 : 'KB', 2 : 'MB'}

def get_file_units(size_in_bytes):
    size = float(size_in_bytes)
    unit = 0
    while True:
        size_in_bytes = size_in_bytes >> 10
        if size_in_bytes == 0:
            break
        unit += 1
    size = f'{round(size / (1 << (unit * 10)), 2)} {file_size_units[unit]}'
    return size

async def image_scaling(image, factor):
    try:
        factor = float(Fraction(factor))
    except ValueError:
        image_utils.delete_img(image)
        raise BadArgument
    if factor <= 0:
        image_utils.delete_img(image)
        raise BadArgument
    size = os.stat(image).st_size
    new_size = size
    if factor > 1:
        new_size = size * factor**2
        if new_size > file_size_limit:
            image_utils.delete_img(image)
            raise UserInputError
    display = True
    if new_size > display_file_size_limit:
        display = False
    im = Image.open(image)
    try:
        output = ImageOps.scale(im, factor)
    except ValueError:
        im.close()
        image_utils.delete_img(image)
        raise UserInputError
    output.save(image)
    return display

async def image_resizing(image, width, height):
    try:
        width = int(width)
        height = int(height)
    except ValueError:
        image_utils.delete_img(image)
        raise BadArgument
    if width <= 0 or height <= 0 or width > 65500 or height > 65500:
        image_utils.delete_img(image)
        raise BadArgument
    im = Image.open(image)
    old_width = im.width
    old_height = im.height
    size = os.stat(image).st_size
    new_size = size
    if width > old_width or height > old_height:
        factor = width * height / (old_width * old_height)
        new_size = size * factor
        if new_size > file_size_limit:
            im.close()
            image_utils.delete_img(image)
            raise UserInputError
    display = True
    if new_size > display_file_size_limit:
        display = False
    output = im.resize((width, height))
    output.save(image)
    return display

async def image_rotation(image, degree):
    try:
        degree = float(degree)
    except ValueError:
        image_utils.delete_img(image)
        raise BadArgument
    degree = degree % 360
    im = Image.open(image)
    output = im.rotate(degree,expand=True)
    output.save(image)

async def image_flip(image, direction):
    if direction != '0' and direction != '1':
        image_utils.delete_img(image)
        raise BadArgument
    direction = int(direction)
    im = Image.open(image)
    output = im.transpose(direction)
    output.save(image)

async def image_compression(image, rate):
    old_file_size = os.stat(image).st_size
    im = Image.open(image)
    new_file_name = None
    if im.format != 'JPEG':
        im = im.convert('RGB')
        new_file_name = image[:-3] + "jpg"
    try:
        rate = float(rate)
    except ValueError:
        im.close()
        image_utils.delete_img(image)
        raise BadArgument
    if rate < 0 or rate > 1:
        im.close()
        image_utils.delete_img(image)
        raise BadArgument
    if (new_file_name == None):
        qlt = int(rate*default_quality)
    else:
        qlt = int(rate*100)

    if (new_file_name == None):
        im.save(image, quality=qlt)
        new_file_size = get_file_units(os.stat(image).st_size)
    else:
        im.save(new_file_name, quality=qlt)
        new_file_size = get_file_units(os.stat(new_file_name).st_size)
    old_file_size = get_file_units(old_file_size)
    return (old_file_size, new_file_size, new_file_name)

async def image_edge_detect(image):
    im = Image.open(image)
    im = im.convert("L")
    output = im.filter(ImageFilter.Kernel((5,5), (1, 1, 1, 1, 1,
                                                  1, 1, 1, 1, 1,
                                                  1, 1, -24, 1, 1,
                                                  1, 1, 1, 1, 1,
                                                  1, 1, 1, 1, 1), 1, 0))
    output.save(image)

def are_image_paths_valid(image_paths):
    image_paths = image_paths.split()
    is_valid = True
    index = 0
    for i in range(0, len(image_paths)):
        try:
            image_paths[i] = image_utils.download_img(image_paths[i])
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

def clear_all_images(image_paths):
    for img_path in image_paths:
        image_utils.delete_img(img_path)

async def gif_create(image_paths):
    is_valid, image_paths = are_image_paths_valid(image_paths)
    if not is_valid or len(image_paths) == 1:
        raise BadArgument
    im = Image.open(image_paths[0])
    width, height = im.width, im.height
    images = []
    for i in range(1, len(image_paths)):
        img_path = image_paths[i]
        img = Image.open(img_path)
        img = img.resize((width, height))
        images.append(img)
        img.save(img_path)
    im.save(default_gif_path, save_all=True, append_images=images, duration=500, loop=0)
    clear_all_images(image_paths)

async def gif_append_image(gif_path, image_paths):
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
            for j, frame in enumerate(img):
                frame[j].resize((width, height))
                images.append(frame[j])
        else:
            img = img.resize((width, height))
            images.append(img)
            img.save(img_path)
    images[0].save(gif_path, save_all=True, append_images=images[1:], duration=500, loop=0)
    clear_all_images(image_paths)