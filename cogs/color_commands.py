from discord.ext import commands
from discord.ext.commands import (
    MissingRequiredArgument,
    TooManyArguments,
    BadArgument,
    CommandInvokeError,
)
from utils.color import Grayscale, Hue

from image_utils import process_command, InvalidURL


class ColorCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="grayscale",
        description="Test that the bot can download images and send them back converted to grayscale",
    )
    async def grayscale(self, ctx, *args):
        await process_command(ctx, Grayscale(), *args)

    @grayscale.error
    async def grayscale_error_handler(self, ctx, error):
        if isinstance(error, (MissingRequiredArgument, TooManyArguments, BadArgument)):
            await ctx.send(f"Usage: {Grayscale().usage}")
        elif isinstance(error, CommandInvokeError):
            if isinstance(error.__cause__, InvalidURL):
                await ctx.send(error.__cause__)
            elif isinstance(error.__cause__, TooManyArguments):
                await ctx.send(f"Too many arguments. Usage: {Grayscale().usage}")
        else:
            await ctx.send(f"Something unexpected happened: {error}")

    @commands.command(
        name="hue",
        description="Test that the bot can download images and send them back with adjusted hue",
    )
    async def hue(self, ctx, change, *args):
        await process_command(ctx, Hue(), *args, change=change)

    @hue.error
    async def hue_error_handler(self, ctx, error):
        if isinstance(error, (MissingRequiredArgument, TooManyArguments, BadArgument)):
            await ctx.send(f"Usage: {Hue().usage}")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Hue change is integer between 0 and 180.")

        else:
            await ctx.send(f"Something unexpected happened: {error}")


async def setup(bot):
    await bot.add_cog(ColorCog(bot))
