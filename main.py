import discord

import os

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    #necessary so the bot doesn't respond to itself
    if message.author == client.user:
        return

    #can generally create 
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

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

    client.run(BOT_TOKEN)