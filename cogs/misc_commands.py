from discord.ext import commands
from discord.ext.commands import MissingRequiredArgument, TooManyArguments, BadArgument, CommandInvokeError
from utils.misc import ImageInfo, Echo

from image_utils import process_command, InvalidURL

class MiscCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="info", description="Prints the data associated with the image")
    async def image_info(self, ctx, *args):
        await process_command(ctx, ImageInfo(), *args, c=ctx)
    
    @image_info.error
    async def image_info_error_handler(self, ctx, error):
        if isinstance(error, (MissingRequiredArgument, TooManyArguments)):
            await ctx.send(f"Usage: {ImageInfo().usage}")
        elif isinstance(error, CommandInvokeError):
            if isinstance(error.__cause__, InvalidURL):
                await ctx.send(error.__cause__)
            elif isinstance(error.__cause__, TooManyArguments):
                await ctx.send(f"Too many arguments. Usage: {ImageInfo().usage}")
        else:
            await ctx.send(f"Something unexpected happened: {error}")

    @commands.command(name="echo", description="Echos back the image")
    async def echo(self, ctx, *args):
        await process_command(ctx, Echo(), *args)

    @echo.error
    async def echo_error_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument, ):
            await ctx.send("Please send a URL linking to your image")
        elif isinstance(error, commands.TooManyArguments):
            await ctx.send("Too many arguments!")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("URL was invalid, make sure to copy the image link")
        else:
            await ctx.send(f"Something unexpected happened: {error}")
    
async def setup(bot):
    await bot.add_cog(MiscCog(bot))