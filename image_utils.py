import discord
from discord.ext.commands import BadArgument

import re
import os
import urllib.request
import cv2
import io

IMG_DIR = "imgs"
MAX_FILENAME_LEN = 128

"""
Adds a user-agent to get around some 403 errors
"""


def spoof_human():
    opener = urllib.request.build_opener()
    opener.addheaders = [
        ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
    urllib.request.install_opener(opener)


"""
Checks if a URL leads to an image file
"""


def is_img_file(url):
    try:
        site = urllib.request.urlopen(url)
        meta = site.info()
        if "image/" in meta["content-type"]:
            return True
        return False
    except ValueError:
        raise BadArgument("Invalid URL")


"""
Attempts to download image from URL
"""
def download_img(url):
    if not is_img_file(url):
        raise BadArgument("Invalid URL: not an image")

    if not os.path.exists(IMG_DIR):
        os.mkdir(IMG_DIR)

    filename = os.path.basename(url)
    if len(filename) >= MAX_FILENAME_LEN:
        filename = "img"
    img_path = os.path.join(IMG_DIR, filename)
    # create an image extension if one wasn't specified in the URL
    __, ext = os.path.splitext(img_path)
    if not ext:
        site = urllib.request.urlopen(url)
        meta = site.info()
        ext = meta["content-type"].split('/')[-1]
        if len(img_path) >= 128:
            img_path = "img"
        img_path = f"{img_path}.{ext}"

    # download the image
    urllib.request.urlretrieve(url, img_path)
    return img_path


"""
Sends an image at the provided image path back to a user
"""


async def send_img_by_path(ctx, img_path):
    with open(img_path, "rb") as img:
        f = discord.File(img, filename=os.path.basename(img_path))
        await ctx.send(file=f)

"""
Sends an image using the provided OpenCV Mat image back to a user
"""


async def send_img_by_mat(ctx, img, filename):
    is_success, buffer = cv2.imencode(".jpg", img)

    if not is_success:
        raise BadArgument("Failed to encode image.")

    io_buf = io.BytesIO(buffer)
    f = discord.File(io_buf, filename)
    await ctx.send(file=f)

"""
Deletes an image at a given path
"""


def delete_img(img_path):
    if os.path.exists(img_path):
        os.remove(img_path)
