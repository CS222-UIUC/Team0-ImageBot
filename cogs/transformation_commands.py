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
            display = transformation.image_scaling(img_path, factor)
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
            display = transformation.image_resizing(img_path, width, height)
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


    
async def setup(bot):
    await bot.add_cog(TransformationCog(bot))