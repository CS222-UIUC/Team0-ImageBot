from discord.ext import commands
from utils import color

from image_utils import process_command

class ColorCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="grayscale", description="Test that the bot can download images and send them back converted to grayscale")
    async def grayscale(self, ctx, *args):
        await process_command(ctx, color.Grayscale(), *args)

    @grayscale.error
    async def grayscale_error_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please send a URL linking to your image")
        else:
            await ctx.send(f"Something unexpected happened: {error}")

async def setup(bot):
    await bot.add_cog(ColorCog(bot))