import discord
from discord.ext.commands import BadArgument, TooManyArguments

import cv2
import io
import os
import urllib.request

from command import Command

IMG_DIR = "imgs"
MAX_FILENAME_LEN = 128

"""
This dict keeps track of the last used image path for each channel
"""
last_used_image_dict = {}

"""
clear last used image dict, and delete all the saved images.
"""
def clear_image_cache():
    for channel in last_used_image_dict:
        delete_file(last_used_image_dict[channel])
        last_used_image_dict.pop(channel)

class InvalidURL(Exception):
    pass

"""
Adds a user-agent to get around some 403 errors
"""
def spoof_human():
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
    urllib.request.install_opener(opener)

"""
Wrapper function for generally processing commands

Parameters:
    ctx: the message context
    command (command.Command): function to be applied to the image.
        - Takes in an img_path and the keyword arguments
    args: the URL if it exists
    kwargs: the keyword arguments needed to run func
"""

async def process_command(ctx, command, *args, **kwargs):
    if len(args) == 0:
        #image not sent as link
        attachments = ctx.message.attachments
        if len(attachments) == 0:
            # no image linked
            await process_url(ctx, 0, command.command, **kwargs)
        else: 
            # image sent as attachment
            for img in attachments:
                await process_url(ctx, img.url, command.command, **kwargs)
    elif len(args) == 1: 
        # image sent as link
        await process_url(ctx, args[0], command.command, **kwargs)
    else:
        raise TooManyArguments
"""
Applies func to the image at a url
"""
async def process_url(ctx, url, func, **kwargs):
    if (url == 0):
        if (ctx.channel in last_used_image_dict):
            url = last_used_image_dict[ctx.channel]
        else:
            await ctx.send(("Sorry, I couldn't find an image or an image link in your message, or a recently used image in this channel"))
            return
    in_path = download_img(url)
    
    out_path = await func(in_path, **kwargs)
    await send_file_by_path(ctx, out_path)
    delete_file(in_path)
    delete_file(out_path)

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
        raise InvalidURL(f"Invalid URL {url}: Could not open site")


"""
Attempts to download image from URL
"""
def download_img(url, dir=IMG_DIR):
    if not is_img_file(url):
        raise InvalidURL(f"Invalid URL {url}: not an image")

    if not os.path.exists(dir):
        os.mkdir(dir)

    filename = os.path.basename(url)
    if len(filename) >= MAX_FILENAME_LEN:
        filename = "img"
    img_path = os.path.join(dir, filename)
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
    return os.path.abspath(img_path)


"""
Sends an image at the provided image path back to a user
"""
async def send_file_by_path(ctx, img_path):
    with open(img_path, "rb") as img:
        f = discord.File(img, filename=os.path.basename(img_path))
        m = (await ctx.send(file=f))
        last_used_image_dict[ctx.channel] = str(m.attachments[0])

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
def delete_file(img_path):
    if os.path.exists(img_path):
        os.remove(img_path)
