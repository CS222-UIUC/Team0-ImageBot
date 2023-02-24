import discord

import re
import os
import urllib.request

img_dir = "imgs"

def is_img_file(url):
    img_formats = ("image/png", "image/jpeg", "image/gif")
    try:
        site = urllib.request.urlopen(url)
        meta = site.info()
        if meta["content-type"] in img_formats:
            return True
        return False
    except ValueError:
        raise discord.ext.commands.BadArgument("Invalid URL")

def download_img(url):
    if not os.path.exists(img_dir):
        os.mkdir(img_dir)
    if not is_img_file(url):
        raise discord.ext.commands.BadArgument("Invalid URL")
    try:
        filename = os.path.join(img_dir, os.path.basename(url))
        urllib.request.urlretrieve(url, filename)
    except (ValueError, IsADirectoryError) as e:
        raise discord.ext.commands.BadArgument("Invalid URL")


async def send_img(ctx, img_path):
    try:
        with open(img_path, "rb") as img:
            f = discord.File(img, filename = os.path.basename(img_path))
            await ctx.send(file = f)
    except IsADirectoryError:
        raise discord.ext.commands.BadArgument("Invalid URL")

def delete_img(img_path):
    if os.path.exists(img_path):
        os.remove(img_path)