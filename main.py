import discord
from discord.ext import commands
from discord import app_commands
from fractions import Fraction

import os

import image_utils
from utils import scaling

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents = intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command(name="test_image", description="Test that the bot can download images and send them back")
async def test_image(ctx, url):
    img_path = image_utils.download_img(url)

    await image_utils.send_img(ctx, img_path)
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

@bot.command(name="scale", description="scale image by factor or by width and height")
async def scale_image(ctx, *args):
    length = len(args)
    if length == 2:
        try:
            factor = float(Fraction(args[0]))
        except ValueError:
            await ctx.send("Factor is not a real number. Usage: $scale [factor] [url]")
            return
        url = args[1]
    elif length == 3:
        try:
            width = int(args[0])
            height = int(args[1])
        except ValueError:
            await ctx.send("Width and height are integers. Usage: $scale [width] [height] [url]")
            return
        url = args[2]
    else:
        await ctx.send("Usage: $scale [factor] [url], or $scale [width] [height] [url]")
        return
    img_path = image_utils.download_img(url)
    if length == 2:
        scaling.image_scaling_by_factor(img_path, factor)
    else:
        scaling.image_scaling_by_width_and_height(img_path, width, height)
    try:
        await image_utils.send_img(ctx, img_path)
    except discord.HTTPException:
        await ctx.send("Scaled image exceeds file size limit. Please choose a smaller factor or smaller width and height")
    image_utils.delete_img(img_path)

if __name__ == "__main__":
    #heroku - get token from environment variable
    if "IMAGE_BOT_TOKEN" in os.environ:
        BOT_TOKEN = os.environ["IMAGE_BOT_TOKEN"]
    #local dev - get token from BOT_TOKEN.txt
    elif os.path.exists("./BOT_TOKEN.txt"):
        with open("BOT_TOKEN.txt", "r") as token_file:
            BOT_TOKEN = token_file.read()
    else:
        raise RuntimeError("Could not find token")

    image_utils.spoof_human()
    
    bot.run(BOT_TOKEN)