from PIL import ImageOps, Image
from discord.ext.commands import BadArgument
from discord.ext.commands import UserInputError
from fractions import Fraction
import os

import image_utils

file_size_limit = 1 << 26 # 64 MB
display_file_size_limit = 1 << 23 # 8 MB
default_gif_path = f"{os.getcwd()}\imgs\default.gif"

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
    try:
        direction = int(direction)
    except ValueError:
        image_utils.delete_img(image)
        raise BadArgument
    if direction != 0 and direction != 1:
        image_utils.delete_img(image)
        raise BadArgument
    im = Image.open(image)
    output = im.transpose(direction)
    output.save(image)

def are_image_paths_valid(image_paths):
    image_paths = image_paths.split()
    is_valid = True
    index = 0
    print(image_paths)
    for i in range(0, len(image_paths)):
        try:
            image_utils.download_img(image_paths[i])
        except BadArgument:
            index = i
            is_valid = False
            break
    print(image_paths)
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
    im.save(default_gif_path, save_all=True, append_images=image_paths[1:])
    clear_all_images(image_paths)

    
async def gif_append_image(gif_path, image_paths):
    is_valid, image_paths = are_image_paths_valid(image_paths)
    if not is_valid:
        raise BadArgument
    im = Image.open(gif_path)
    print(im.format)
    im.save(gif_path, save_all=True, append_images=image_paths)
    clear_all_images(image_paths)
    