from PIL import Image
from discord.ext.commands import BadArgument

import image_utils

def image_flip(image, direction):
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