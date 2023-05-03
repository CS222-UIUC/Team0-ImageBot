from discord.ext import commands
from utils.draw import DrawLine, DrawRect, SampleColor, PickColor
from discord.ext.commands import MissingRequiredArgument, TooManyArguments, BadArgument, CommandInvokeError

from image_utils import process_command, InvalidURL

class DrawCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="line", description="Bot draws line on top of image from point A to B with a given thickness")
    async def line(self, ctx, x1, y1, x2, y2, width, *args):
        await process_command(ctx, DrawLine(), *args, start=(x1, y1), stop=(x2, y2), width=width)

    @line.error
    async def line_error_handler(self, ctx, error):
        if isinstance(error, (MissingRequiredArgument, TooManyArguments)):
            await ctx.send(f"Usage: {DrawLine().usage}")
        elif isinstance(error, CommandInvokeError):
            if isinstance(error.__cause__, InvalidURL):
                await ctx.send(error.__cause__)
            elif isinstance(error.__cause__, TooManyArguments):
                await ctx.send(f"Too many arguments. Usage: {DrawLine().usage}")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Width must be a positive integer")
        elif isinstance(error, commands.UserInputError):
            await ctx.send("Arguments must be integers")
        else:
            await ctx.send(f"Something unexpected happened: {error}")
    
    

    @commands.command(name="rect", description="Bot draws rectangle on top of image bounded by points A and B with a given thickness")
    async def rect(self, ctx, x1, y1, x2, y2, width, *args):
        await process_command(ctx, DrawRect(), *args, start=(x1, y1), stop=(x2, y2), width=width)

    @rect.error
    async def rect_error_handler(self, ctx, error):
        if isinstance(error, (MissingRequiredArgument, TooManyArguments)):
            await ctx.send(f"Usage: {DrawRect().usage}")
        elif isinstance(error, CommandInvokeError):
            if isinstance(error.__cause__, InvalidURL):
                await ctx.send(error.__cause__)
            elif isinstance(error.__cause__, TooManyArguments):
                await ctx.send(f"Too many arguments. Usage: {DrawRect().usage}")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Width must be a positive integer")
        elif isinstance(error, commands.UserInputError):
            await ctx.send("Arguments must be integers")
        else:
            await ctx.send(f"Something unexpected happened: {error}")


    # Note: this command breaks standards, as it does not take an image input but sends back an output
    @commands.command(name="pick_color", description="Sets the color used for future draw commands")
    async def pick_color(self, ctx, r, g, b):
        await PickColor.pick_color(ctx, color=(r, g, b))

    @pick_color.error
    async def pick_color_error_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.TooManyArguments):
            await ctx.send("Usage: $pick_color [r] [g] [b]")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Each color value must be an integer")
        else:
            await ctx.send(f"Something unexpected happened: {error}")


    @commands.command(name="sample_color", description="Sets the color used for future draw commands to the dominant color in a given image")
    async def sample_color(self, ctx, n_colors, *args):
        await process_command(ctx, SampleColor(), *args, n_colors=n_colors)

    @sample_color.error
    async def sample_color_error_handler(self, ctx, error):
        if isinstance(error, (MissingRequiredArgument, TooManyArguments)):
            await ctx.send(f"Usage: {SampleColor().usage}")
        elif isinstance(error, CommandInvokeError):
            if isinstance(error.__cause__, InvalidURL):
                await ctx.send(error.__cause__)
            elif isinstance(error.__cause__, TooManyArguments):
                await ctx.send(f"Too many arguments. Usage: {SampleColor().usage}")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Number of colors must be a positive integer")
        else:
            await ctx.send(f"Something unexpected happened: {error}")


async def setup(bot):
    await bot.add_cog(DrawCog(bot))