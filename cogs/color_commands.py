from discord.ext import commands
from discord.ext.commands import MissingRequiredArgument, TooManyArguments, BadArgument, CommandInvokeError
from utils.color import Grayscale

from image_utils import process_command, InvalidURL

class ColorCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="grayscale", description="Test that the bot can download images and send them back converted to grayscale")
    async def grayscale(self, ctx, *args):
        await process_command(ctx, Grayscale(), *args)

    @grayscale.error
    async def grayscale_error_handler(self, ctx, error):
        if isinstance(error, (MissingRequiredArgument, TooManyArguments, BadArgument)):
            await ctx.send(f"Usage: {Grayscale().usage}")
        elif isinstance(error, CommandInvokeError):
            if isinstance(error.__cause__, InvalidURL):
                await ctx.send(error.__cause__)
        else:
            await ctx.send(f"Something unexpected happened: {error}")

async def setup(bot):
    await bot.add_cog(ColorCog(bot))