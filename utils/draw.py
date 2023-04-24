import cv2
import image_utils
import os
import numpy as np
from discord.ext import commands
from command import Command
from PIL import Image
from PIL.ExifTags import TAGS
import hashlib


curr_color = (0, 0, 0)
SWATCH_SIZE = 100
SWATCH_PATH = os.path.join(image_utils.IMG_DIR, "swatch.jpg")

class DrawLine(Command):
    def __init__(self):
        super().__init__("$line [x1] [y1] [x2] [y2] [width] [url]")
    
    async def command(self, img_path, start, stop, width):
        img_path = DrawLine.drawline(img_path, start, stop, width)
        return img_path
    
    """draws black line between given points"""
    def drawline(img_path, start, stop, width):
        try:
            p1 = (int(start[0]), int(start[1]))
            p2 = (int(stop[0]), int(stop[1]))
            width = int(width)
        except:
            image_utils.delete_file(img_path)
            raise commands.UserInputError

        if (width <= 0):
            image_utils.delete_file(img_path)
            raise commands.BadArgument
        img = cv2.imread(img_path)
        cv2.line(img, p1, p2, curr_color, width)
        cv2.imwrite(img_path, img)

        return img_path


class DrawRect(Command):
    def __init__(self):
        super().__init__("$rect [x1] [y1] [x2] [y2] [width] [url]")
    
    async def command(self, img_path, start, stop, width):
        await DrawRect.drawrect(img_path, start, stop, width)
        return img_path
    
    """draws rect bounded by two points"""
    async def drawrect(img_path, start, stop, width):
        # print(start, stop, width)
        try:
            p1 = (int(start[0]), int(start[1]))
            p2 = (int(stop[0]), int(stop[1]))
            width = int(width)
        except:
            image_utils.delete_file(img_path)
            raise commands.UserInputError

        if (width <= 0):
            image_utils.delete_file(img_path)
            raise commands.BadArgument
        
        img = cv2.imread(img_path)
        cv2.rectangle(img, p1, p2, curr_color, width)
        cv2.imwrite(img_path, img)
        return img_path


class PickColor(Command):
    def __init__(self):
        super().__init__("$pick_color [r] [g] [b]")
    
    # async def command(self, img_path, factor, cntx):
    #     display = await self.pick_color(img_path, factor)
    #     if not display:
    #         await cntx.send("To see the image, please copy the link and open it in a browser")
    #     return img_path
    
    # Note: this command breaks standards, as it does not take an image input, but sends back an output
    async def pick_color(ctx, color):
        global curr_color
        try:
            curr_color = (int(color[0])%256, int(color[1])%256, int(color[2])%256)
        except:
            raise commands.BadArgument
        # curr_color = color
        if not os.path.exists(image_utils.IMG_DIR):
            os.mkdir(image_utils.IMG_DIR)

        blank_image = np.zeros((SWATCH_SIZE, SWATCH_SIZE, 3), np.uint8)
        blank_image[:,:] = curr_color

        await image_utils.send_img_by_mat(ctx, blank_image, "swatch.jpg")

class SampleColor(Command):
    def __init__(self):
        super().__init__("$sample_color [num_colors] [url]")
    
    async def command(self, img_path, n_colors):
        await SampleColor.sample_color(img_path, n_colors)
        return img_path
    
    async def sample_color(img_path, n_colors):
        try:
            n_colors = int(n_colors)
        except:
            image_utils.delete_file(img_path)
            raise commands.BadArgument
        global curr_color
        img = cv2.imread(img_path)
        pixels = np.float32(img.reshape(-1, 3))

        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
        flags = cv2.KMEANS_RANDOM_CENTERS

        _, labels, palette = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
        _, counts = np.unique(labels, return_counts=True)

        dominant = palette[np.argmax(counts)]
        curr_color = (int(dominant[0]), int(dominant[1]), int(dominant[2]))

        blank_image = np.zeros((SWATCH_SIZE, SWATCH_SIZE, 3), np.uint8)
        blank_image[:,:] = curr_color
        cv2.imwrite(img_path, blank_image)
        return img_path

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





