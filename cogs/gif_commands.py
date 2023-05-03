from discord.ext import commands
from utils.gif import GifCreate, GifAppend
from discord.ext.commands import MissingRequiredArgument, TooManyArguments, BadArgument
from discord.ext.commands import MissingRequiredArgument, TooManyArguments, BadArgument, CommandInvokeError

from image_utils import process_command, InvalidURL

class GIFCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    """Create gifs"""    
    @commands.command(name="create_gif", description="create a gif from input images")
    async def create_gif(self, ctx, image_paths, *args):
        await process_command(ctx, GifCreate(), *args, image_paths=image_paths)

    @create_gif.error
    async def create_error_handler(self, ctx, error):
        if isinstance(error, (MissingRequiredArgument, TooManyArguments)):
            await ctx.send(f"Usage: {GifCreate().usage}")
        elif isinstance(error, CommandInvokeError):
            if isinstance(error.__cause__, InvalidURL):
                await ctx.send(error.__cause__)
            elif isinstance(error.__cause__, TooManyArguments):
                await ctx.send(f"Too many arguments. Usage: {GifCreate().usage}")
        elif isinstance(error, BadArgument):
            await ctx.send("Make sure all urls are valid and image urls are separated by spaces and in double quotation")
        else:
            await ctx.send(f"Something unexpected happened: {error}")
    
    """Append gifs"""
    @commands.command(name="append_gif", description="append input images to a gif")
    async def append_gif(self, ctx, image_paths, *args):
        await process_command(ctx, GifAppend(), *args, image_paths=image_paths)

    @append_gif.error
    async def append_error_handler(self, ctx, error):
        if isinstance(error, (MissingRequiredArgument, TooManyArguments)):
            await ctx.send(f"Usage: {GifAppend().usage}")
        elif isinstance(error, CommandInvokeError):
            if isinstance(error.__cause__, InvalidURL):
                await ctx.send(error.__cause__)
            elif isinstance(error.__cause__, TooManyArguments):
                await ctx.send(f"Too many arguments. Usage: {GifAppend().usage}")
        elif isinstance(error, BadArgument):
            await ctx.send("Make sure all urls are valid and image urls are separated by spaces and in double quotation")
        else:
            await ctx.send(f"Something unexpected happened: {error}")
    
async def setup(bot):
    await bot.add_cog(GIFCog(bot))