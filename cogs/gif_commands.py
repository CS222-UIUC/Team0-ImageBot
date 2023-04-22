from discord.ext import commands
from utils.gif import GifCreate, GifAppend
from discord.ext.commands import MissingRequiredArgument, TooManyArguments, BadArgument

from image_utils import process_command

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
        elif isinstance(error, BadArgument):
            await ctx.send(f"Usage: {GifCreate().usage}")
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
        elif isinstance(error, BadArgument):
            await ctx.send(f"Usage: {GifAppend().usage}")
        else:
            await ctx.send(f"Something unexpected happened: {error}")
    
async def setup(bot):
    await bot.add_cog(GIFCog(bot))