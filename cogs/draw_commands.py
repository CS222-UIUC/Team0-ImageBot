from discord.ext import commands
from utils import draw

from image_utils import process_command

class DrawCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="line", description="Bot draws line on top of image from point A to B with a given thickness")
    async def line(self, ctx, x1, y1, x2, y2, width, *args):
        await process_command(ctx, draw.drawline, *args, start=(x1, y1), stop=(x2, y2), width=width)

    @line.error
    async def draw_error_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.TooManyArguments):
            await ctx.send("Usage: $line [x1] [y1] [x2] [y2] [width] [url]")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Width must be a positive integer")
        elif isinstance(error, commands.UserInputError):
            await ctx.send("Arguments must be integers")
        else:
            await ctx.send(f"Something unexpected happened: {error}")
    
    

    @commands.command(name="rect", description="Bot draws rectangle on top of image bounded by points A and B with a given thickness")
    async def rect(self, ctx, x1, y1, x2, y2, width, *args):
        await process_command(ctx, draw.drawrect, *args, start=(x1, y1), stop=(x2, y2), width=width)

    @rect.error
    async def rect_error_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.TooManyArguments):
            await ctx.send("Usage: $rect [x1] [y1] [x2] [y2] [width] [url]")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Width must be a positive integer")
        elif isinstance(error, commands.UserInputError):
            await ctx.send("Arguments must be integers")
        else:
            await ctx.send(f"Something unexpected happened: {error}")

async def setup(bot):
    await bot.add_cog(DrawCog(bot))