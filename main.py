import discord
from discord.ext import commands
from discord import app_commands

import os

import image_utils

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents = intents)

@bot.event
async def setup_hook():
    await bot.tree.sync(guild = discord.Object(id = 1072586003094712370))

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.hybrid_command(name="test_image", description="This is a test")
async def test_image(ctx, url):
    image_utils.download_img(url)

    img_name = os.path.basename(url)
    img_path = os.path.join("imgs/", img_name)
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

    bot.run(BOT_TOKEN)