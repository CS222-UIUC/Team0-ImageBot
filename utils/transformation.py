from PIL import ImageOps, Image, ImageShow
from discord.ext.commands import BadArgument
from discord.ext.commands import UserInputError
from fractions import Fraction
import os

import image_utils

file_size_limit = 1 << 26 # 64 MB
display_file_size_limit = 1 << 23 # 8 MB
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
    if im.format != 'JPEG':
        im.close()
        image_utils.delete_img(image)
        raise BadArgument
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
    qlt = int(rate*default_quality)
    im.save(image,quality=qlt)
    new_file_size = get_file_units(os.stat(image).st_size)
    old_file_size = get_file_units(old_file_size)
    return (old_file_size, new_file_size)