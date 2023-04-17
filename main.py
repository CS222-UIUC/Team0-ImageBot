import asyncio
import os
import signal
import sys
import shutil

import discord
from discord.ext import commands

from image_utils import process_command, spoof_human

IMG_DIR = "imgs"

def singal_handler(signum, frame):
    for filename in os.listdir(IMG_DIR):
        filepath = os.path.join(IMG_DIR, filename)
        if os.path.isfile(filepath) or os.path.islink(filepath):
            os.unlink(filepath)
        elif os.path.isdir(filepath):
            shutil.rmtree(filepath)
    sys.exit(0)

signal.signal(signal.SIGINT, singal_handler)

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

@bot.command(name="echo", description="Echos back the image")
async def echo(ctx, *args):
    await process_command(ctx, test_image_fun, *args)

@echo.error
async def echo_error_handler(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please send a URL linking to your image")
    elif isinstance(error, commands.TooManyArguments):
        await ctx.send("Too many arguments!")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("URL was invalid, make sure to copy the image link")
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

    spoof_human()

    cogs = ["color", "transformation", "draw"]
    for cog in cogs:
        asyncio.run(bot.load_extension(f"cogs.{cog}_commands"))
    bot.run(BOT_TOKEN)
