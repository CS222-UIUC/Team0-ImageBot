import asyncio
import os

import discord
from discord.ext import commands

from image_utils import process_command, spoof_human
from cogs.color_commands import ColorCog
from utils import color
from utils import scaling

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

"""
Basic func example, does nothing to the image
"""
async def test_image_fun(img_path):
    return

@bot.command(name="test_image", description="Test that the bot can download images and send them back")
async def test_image(ctx, *args):
    await process_command(ctx, test_image_fun, *args)

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
async def scale_image(ctx, factor, *args):
    async def scaling_wrapper(img_path, factor):
        display = scaling.image_scaling(img_path, factor)
        if not display:
            await ctx.send("To see the image, please copy the link and open it in a browser")
    await process_command(ctx, scaling_wrapper, *args, factor=factor)

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
async def resize_image(ctx, width, height, *args):
    async def resize_image_wrapper(img_path, width, height):
        display = scaling.image_resizing(img_path, width, height)
        if not display:
            await ctx.send("To see the image, please copy the link and open it in a browser")
    await process_command(ctx, resize_image_wrapper, *args, width=width, height=height)

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

"""
@bot.command(name="grayscale", description="Test that the bot can download images and send them back converted to grayscale")
async def grayscale(ctx, *args):
    await process_command(ctx, color.grayscale, *args)

@grayscale.error
async def grayscale_error_handler(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please send a URL linking to your image")
    else:
        await ctx.send(f"Something unexpected happened: {error}")
"""

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

    spoof_human()
    asyncio.run(bot.load_extension("cogs.color_commands"))
    bot.run(BOT_TOKEN)
