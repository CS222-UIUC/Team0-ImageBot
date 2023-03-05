from discord.ext import commands
from utils import draw

from image_utils import process_command

class DrawCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="line", description="Bot draws line on top of image from point A to B with a given thickness")
    async def line(self, ctx, *args):
        await process_command(ctx, draw.drawline, *args)

    @draw.error
    async def draw_error_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please send a URL linking to your image")
        else:
            await ctx.send(f"Something unexpected happened: {error}")

async def setup(bot):
    await bot.add_cog(DrawCog(bot))