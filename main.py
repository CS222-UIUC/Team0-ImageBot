import discord
from discord.ext import commands
from discord import app_commands
import cv2
import io
import os

import image_utils
from utils import scaling
from utils import rotation
from utils import flip

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.command(name="test_image", description="Test that the bot can download images and send them back")
async def test_image(ctx, url):
    img_path = image_utils.download_img(url)

    await image_utils.send_img_by_path(ctx, img_path)
    image_utils.delete_img(img_path)


@test_image.error
async def image_error_handler(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please send a URL linking to your image")
    elif isinstance(error, commands.TooManyArguments):
        await ctx.send("Too many arguments!")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("URL was invalid, make sure to copy the image link")
    else:
        await ctx.send(f"Something unexpected happened: {error}")

@bot.command(name="scale", description="scale image by factor")
async def scale_image(ctx, factor, url):
    img_path = image_utils.download_img(url)
    display = scaling.image_scaling(img_path, factor)
    if not display:
        await ctx.send("To see the image, please copy the link and open it in a browser")
    await image_utils.send_img_by_path(ctx, img_path)
    image_utils.delete_img(img_path)

@scale_image.error
async def scale_error_handler(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.TooManyArguments):
        await ctx.send("Usage: $scale [factor] [url]")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Factor needs to be a real positive number")
    elif isinstance(error, commands.UserInputError):
        await ctx.send("Factor is either too small or too big. Please choose an appropriate factor")
    else:
        await ctx.send(f"Something unexpected happened: {error}")

@bot.command(name="resize", description="resize image by width and height")
async def resize_image(ctx, width, height, url):
    img_path = image_utils.download_img(url)
    display = scaling.image_resizing(img_path, width, height)
    if not display:
        await ctx.send("To see the image, please copy the link and open it in a browser")
    await image_utils.send_img_by_path(ctx, img_path)
    image_utils.delete_img(img_path)

@resize_image.error
async def resize_error_handler(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.TooManyArguments):
        await ctx.send("Usage: $resize [width] [height] [url]")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Width and Height need to be positive integers less than or equal to 65500")
    elif isinstance(error, commands.UserInputError):
        await ctx.send("Resized image exceeds file size limit. Please choose smaller width and height")
    else:
        await ctx.send(f"Something unexpected happened: {error}")

@bot.command(name="rotate", description="rotate image by degrees counterclockwise if positive, clockwise if negative")
async def rotate_image(ctx, degree, url):
    img_path = image_utils.download_img(url)
    rotation.image_rotation(img_path, degree)
    await image_utils.send_img_by_path(ctx, img_path)
    image_utils.delete_img(img_path)

@rotate_image.error
async def rotate_error_handler(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.TooManyArguments):
        await ctx.send("Usage: $rotate [degree] [url]. Positive degrees for rotation counterclockwise, and negative degrees clockwise")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Degree needs to be a real number")
    else:
        await ctx.send(f"Something unexpected happened: {error}")

@bot.command(name="flip", description="flip image left right or top bottom")
async def flip_image(ctx, direction, url):
    img_path = image_utils.download_img(url)
    flip.image_flip(img_path, direction)
    await image_utils.send_img_by_path(ctx, img_path)
    image_utils.delete_img(img_path)

@flip_image.error
async def flip_error_handler(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.TooManyArguments):
        await ctx.send("Usage: $flip [direction] [url]. Direction equals 0 for flipping left and right, and 1 for flipping up and down")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Direction takes either 0 or 1")
    else:
        await ctx.send(f"Something unexpected happened: {error}")

@bot.command(name="grayscale", description="Test that the bot can download images and send them back converted to grayscale")
async def grayscale(ctx, url):

    img_path = image_utils.download_img(url)
    img = cv2.imread(img_path, 0)
    await image_utils.send_img_by_mat(ctx, img, "grayscale.jpg")
    image_utils.delete_img(img_path)

@grayscale.error
async def grayscale_error_handler(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please send a URL linking to your image")
    else:
        await ctx.send(f"Something unexpected happened: {error}")

if __name__ == "__main__":
    # heroku - get token from environment variable
    if "IMAGE_BOT_TOKEN" in os.environ:
        BOT_TOKEN = os.environ["IMAGE_BOT_TOKEN"]
    # local dev - get token from BOT_TOKEN.txt
    elif os.path.exists("./BOT_TOKEN.txt"):
        with open("BOT_TOKEN.txt", "r") as token_file:
            BOT_TOKEN = token_file.read()
    else:
        raise RuntimeError("Could not find token")

    image_utils.spoof_human()

    bot.run(BOT_TOKEN)
