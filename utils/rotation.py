from PIL import Image
from discord.ext.commands import BadArgument

import image_utils

def image_rotation(image, degree):
    try:
        degree = float(degree)
    except ValueError:
        image_utils.delete_img(image)
        raise BadArgument
    degree = degree % 360
    im = Image.open(image)
    output = im.rotate(degree,expand=True)
    output.save(image)