from PIL import ImageOps, Image
import numpy as np

def image_scaling_by_factor(image, factor):
    im = Image.open(image)
    output = ImageOps.scale(im, factor)
    output.save(image)

def image_scaling_by_width_and_height(image, width, height):
    im = Image.open(image)
    output = im.resize((width, height))
    output.save(image)