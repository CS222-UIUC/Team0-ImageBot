import cv2
import image_utils
import os
import numpy as np
from discord.ext import commands
from command import Command
from PIL import Image
from PIL.ExifTags import TAGS
import hashlib

class ImageInfo(Command):
    def __init__(self):
        super().__init__("$info [url]")
    
    async def command(self, img_path, c):
        await ImageInfo.image_info(img_path, c)
        return img_path
    
    async def image_info(img_path, ctx):
        img = Image.open(img_path)
        await ctx.send("Dimensions: " + str(img.height) + " x " + str(img.width))

        with open(img_path, "rb") as f:
            img_hash = hashlib.md5()
            while chunk := f.read(8192):
                img_hash.update(chunk)
        await ctx.send("Hash: " + str(img_hash.hexdigest()))

        exifdata = img.getexif()
        
        if (len(exifdata) == 0):
            await ctx.send("No metadata found")
        for tagid in exifdata:
            tagname = TAGS.get(tagid, tagid)
            value = exifdata.get(tagid)
            await ctx.send(str(tagname) + ": " + str(value))

class Echo(Command):
    def __init__(self):
        super().__init__("$echo [image link/uploaded image]")
    async def command(self, img_path):
        return img_path
