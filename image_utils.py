import discord
from discord.ext.commands import BadArgument

import re
import os
import urllib.request

img_dir = "imgs"

def is_img_file(url):
    try:
        site = urllib.request.urlopen(url)
        meta = site.info()
        if "image/" in meta["content-type"]:
            return True
        return False
    except ValueError:
        raise BadArgument("Invalid URL")

def download_img(url):
    if not is_img_file(url):
        raise BadArgument("Invalid URL: not an image")

    if not os.path.exists(img_dir):
        os.mkdir(img_dir)
    filename = os.path.join(img_dir, os.path.basename(url))
    #create an image extension if one wasn't specified in the URL
    __, ext = os.path.splitext(filename)
    if not ext:
        site = urllib.request.urlopen(url)
        meta = site.info()
        ext = meta["content-type"].split('/')[-1]
        filename = f"{filename}.{ext}"

    #download the image
    urllib.request.urlretrieve(url, filename)
    return filename


async def send_img(ctx, img_path):
    with open(img_path, "rb") as img:
        f = discord.File(img, filename = os.path.basename(img_path))
        await ctx.send(file = f)

def delete_img(img_path):
    if os.path.exists(img_path):
        os.remove(img_path)