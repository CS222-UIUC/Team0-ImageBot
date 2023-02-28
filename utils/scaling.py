from PIL import ImageOps, Image
from discord.ext.commands import BadArgument
from discord.ext.commands import UserInputError
from discord.ext.commands import CommandInvokeError
from fractions import Fraction
import os

file_size_limit = 1 << 26 # 64 MB
display_file_size_limit = 1 << 23 # 8 MB

def image_scaling(image, factor):
    try:
        factor = float(Fraction(factor))
    except ValueError:
        raise BadArgument
    if factor <= 0:
        raise BadArgument
    if factor > 1:
        size = os.stat(image).st_size
        new_size = size * factor**2
        if new_size > file_size_limit:
            raise CommandInvokeError
    display = True
    if new_size > display_file_size_limit:
        display = False
    im = Image.open(image)
    try:
        output = ImageOps.scale(im, factor)
    except ValueError:
        raise UserInputError
    output.save(image)
    return display

def image_resizing(image, width, height):
    try:
        width = int(width)
        height = int(height)
    except ValueError:
        raise BadArgument
    if width <= 0 or height <= 0 or width > 65500 or height > 65500:
        raise BadArgument
    im = Image.open(image)
    old_width = im.width
    old_height = im.height
    if width > old_width or height > old_height:
        size = os.stat(image).st_size
        factor = width * height / (old_width * old_height)
        new_size = size * factor
        if new_size > file_size_limit:
            raise CommandInvokeError
    display = True
    if new_size > display_file_size_limit:
        display = False
    output = im.resize((width, height))
    output.save(image)
    return display