from discord.ext import commands
from utils.transformation import ImageScaling, ImageResizing, ImageRotation, ImageFlip, EdgeDetect, Compress
from discord.ext.commands import MissingRequiredArgument, TooManyArguments, BadArgument, CommandInvokeError

from image_utils import process_command, InvalidURL

class TransformationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Scaling"""
    @commands.command(name="scale", description="scale image by factor")
    async def scale(self, ctx, factor, *args):
        await process_command(ctx, ImageScaling(), *args, factor=factor, cntx=ctx)

    @scale.error
    async def scale_error_handler(self, ctx, error):
        if isinstance(error, (MissingRequiredArgument, TooManyArguments)):
            await ctx.send(f"Usage: {ImageScaling().usage}")
        elif isinstance(error, CommandInvokeError):
            if isinstance(error.__cause__, InvalidURL):
                await ctx.send(error.__cause__)
            elif isinstance(error.__cause__, TooManyArguments):
                await ctx.send(f"Too many arguments. Usage: {ImageScaling().usage}")
        elif isinstance(error, BadArgument):
            await ctx.send("Factor needs to be a real positive number")
        elif isinstance(error, commands.UserInputError):
            await ctx.send("Factor is either too small or too big. Please choose an appropriate factor")
        else:
            await ctx.send(f"Something unexpected happened: {error}")

    """Resizing"""
    @commands.command(name="resize", description="resize image by width and height")
    async def resize_image(self, ctx, width, height, *args):
        await process_command(ctx, ImageResizing(), *args, width=width, height=height, cntx=ctx)

    @resize_image.error
    async def resize_error_handler(self, ctx, error):
        if isinstance(error, (MissingRequiredArgument, TooManyArguments)):
            await ctx.send(f"Usage: {ImageResizing().usage}")
        if isinstance(error.__cause__, InvalidURL):
            if isinstance(error.__cause__, InvalidURL):
                await ctx.send(error.__cause__)
            elif isinstance(error.__cause__, TooManyArguments):
                await ctx.send(f"Too many arguments. Usage: {ImageResizing().usage}")
        elif isinstance(error, BadArgument):
            await ctx.send("Width and Height need to be positive integers less than or equal to 65500")
        elif isinstance(error, commands.UserInputError):
            await ctx.send("Resized image exceeds file size limit. Please choose smaller width and height")
        else:
            await ctx.send(f"Something unexpected happened: {error}")

    """Rotation"""
    @commands.command(name="rotate", description="rotate image by degrees counterclockwise if positive, clockwise if negative")
    async def rotate_image(self, ctx, degree, *args):
        await process_command(ctx, ImageRotation(), *args, degree=degree)

    @rotate_image.error
    async def rotate_error_handler(self, ctx, error):
        if isinstance(error, (MissingRequiredArgument, TooManyArguments)):
            await ctx.send(f"Usage: {ImageRotation().usage}")
        elif isinstance(error, CommandInvokeError):
            if isinstance(error.__cause__, InvalidURL):
                await ctx.send(error.__cause__)
            elif isinstance(error.__cause__, TooManyArguments):
                await ctx.send(f"Too many arguments. Usage: {ImageRotation().usage}")

        elif isinstance(error, BadArgument):
            await ctx.send("Degree needs to be a real number")
        else:
            await ctx.send(f"Something unexpected happened: {error}")

    """Flip"""
    @commands.command(name="flip", description="flip image left right or top bottom")
    async def flip_image(self, ctx, direction, *args):
        await process_command(ctx, ImageFlip(), *args, direction=direction)

    @flip_image.error
    async def flip_error_handler(self, ctx, error):
        if isinstance(error, (MissingRequiredArgument, TooManyArguments)):
            await ctx.send(f"Usage: {ImageFlip().usage}")
        elif isinstance(error, CommandInvokeError):
            if isinstance(error.__cause__, InvalidURL):
                await ctx.send(error.__cause__)
            elif isinstance(error.__cause__, TooManyArguments):
                await ctx.send(f"Too many arguments. Usage: {ImageFlip().usage}")
        elif isinstance(error, BadArgument):
            await ctx.send("Direction takes either 0 or 1")
        else:
            await ctx.send(f"Something unexpected happened: {error}")
    
    """Compression"""
    @commands.command(name="compress", description="compress image by a rate")
    async def compress_image(self, ctx, rate, *args):
        await process_command(ctx, Compress(), *args, rate=rate, cntx=ctx)

    @compress_image.error
    async def compress_error_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.TooManyArguments):
            await ctx.send(f"Usage: {Compress().usage}")
        elif isinstance(error, commands.BadArgument):
            await ctx.send(f"Usage: {Compress().usage}")
        else:
            await ctx.send(f"Something unexpected happened: {error}")

    """Edge detection"""
    @commands.command(name="edge_detect", description="Edge detection of image")
    async def edge_detect_image(self, ctx, *args):
        await process_command(ctx, EdgeDetect(), *args)

    @edge_detect_image.error
    async def edge_detect_error_handler(self, ctx, error):
        if isinstance(error, (MissingRequiredArgument, TooManyArguments)):
            await ctx.send(f"Usage: {EdgeDetect().usage}")
        else:
            await ctx.send(f"Something unexpected happened: {error}")
    
async def setup(bot):
    await bot.add_cog(TransformationCog(bot))