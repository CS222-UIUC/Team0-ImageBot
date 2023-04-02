from discord.ext import commands
from discord.ext.commands import MissingRequiredArgument, TooManyArguments, BadArgument, CommandInvokeError

from utils.effect import Triangulate
from image_utils import process_command, InvalidURL

class EffectCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="triangulate", description="triangulate an image")
    async def triangulate(self, ctx, points, *args):
        await process_command(ctx, Triangulate(), *args, points=int(points))

    @triangulate.error
    async def triangulate_error_handler(self, ctx, error):
        if isinstance(error, (MissingRequiredArgument, TooManyArguments)):
            await ctx.send(f"Usage: {Triangulate().usage}")
        elif isinstance(error, BadArgument):
            await ctx.send(error)
        else:
            await ctx.send(f"Something unexpected happened {error}")

async def setup(bot):
    await bot.add_cog(EffectCog(bot))