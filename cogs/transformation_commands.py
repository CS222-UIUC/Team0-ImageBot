from discord.ext import commands
from utils import transformation

from image_utils import process_command

class TransformationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """
    Scaling
    """
    @commands.command(name="scale", description="scale image by factor")
    async def scale(self, ctx, factor, *args):
        async def scaling_wrapper(img_path, factor):
            display = await transformation.image_scaling(img_path, factor)
            if not display:
                await ctx.send("To see the image, please copy the link and open it in a browser")
        await process_command(ctx, scaling_wrapper, *args, factor=factor)

    @scale.error
    async def scale_error_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.TooManyArguments):
            await ctx.send("Usage: $scale [factor] [url]")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Factor needs to be a real positive number")
        elif isinstance(error, commands.UserInputError):
            await ctx.send("Factor is either too small or too big. Please choose an appropriate factor")
        else:
            await ctx.send(f"Something unexpected happened: {error}")

    """Resizing"""
    @commands.command(name="resize", description="resize image by width and height")
    async def resize_image(self, ctx, width, height, *args):
        async def resize_image_wrapper(img_path, width, height):
            display = await transformation.image_resizing(img_path, width, height)
            if not display:
                await ctx.send("To see the image, please copy the link and open it in a browser")
        await process_command(ctx, resize_image_wrapper, *args, width=width, height=height)

    @resize_image.error
    async def resize_error_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.TooManyArguments):
            await ctx.send("Usage: $resize [width] [height] [url]")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Width and Height need to be positive integers less than or equal to 65500")
        elif isinstance(error, commands.UserInputError):
            await ctx.send("Resized image exceeds file size limit. Please choose smaller width and height")
        else:
            await ctx.send(f"Something unexpected happened: {error}")

    """Rotation"""
    @commands.command(name="rotate", description="rotate image by degrees counterclockwise if positive, clockwise if negative")
    async def rotate_image(self, ctx, degree, *args):
        await process_command(ctx, transformation.image_rotation, *args, degree=degree)

    @rotate_image.error
    async def rotate_error_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.TooManyArguments):
            await ctx.send("Usage: $rotate [degree] [url]. Positive degrees for rotation counterclockwise, and negative degrees clockwise")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Degree needs to be a real number")
        else:
            await ctx.send(f"Something unexpected happened: {error}")

    @commands.command(name="flip", description="flip image left right or top bottom")
    async def flip_image(self, ctx, direction, *args):
        await process_command(ctx, transformation.image_flip, *args, direction=direction)

    @flip_image.error
    async def flip_error_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.TooManyArguments):
            await ctx.send("Usage: $flip [direction] [url]. Direction equals 0 for flipping left and right, and 1 for flipping up and down")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Direction takes either 0 or 1")
        else:
            await ctx.send(f"Something unexpected happened: {error}")
    
    @commands.command(name="edge_detect", description="Edge detection of image")
    async def edge_detect_image(self, ctx, *args):
        await process_command(ctx, transformation.image_edge_detect, *args)

    @edge_detect_image.error
    async def edge_detect_error_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.TooManyArguments):
            await ctx.send("Usage: $edge_detect [url]")
        else:
            await ctx.send(f"Something unexpected happened: {error}")
    
async def setup(bot):
    await bot.add_cog(TransformationCog(bot))