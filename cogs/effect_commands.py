from discord.ext import commands
from discord.ext.commands import MissingRequiredArgument, TooManyArguments, BadArgument, CommandInvokeError

from utils.effect import Triangulate, TriAnimation, Voronoi, VoronoiAnimation
from image_utils import process_command, InvalidURL

class EffectCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="triangulate", description="triangulate an image")
    async def triangulate(self, ctx, points, *args):
        await process_command(ctx, Triangulate(), *args, points=points)
    
    @triangulate.error
    async def triangulate_error_handler(self, ctx, error):
        if isinstance(error, (MissingRequiredArgument, TooManyArguments)):
            await ctx.send(f"Usage: {Triangulate().usage}")
        elif isinstance(error, BadArgument):
            await ctx.send(error)
        elif isinstance(error, CommandInvokeError):
            if isinstance(error.__cause__, InvalidURL):
                await ctx.send(error.__cause__)
            elif isinstance(error.__cause__, TooManyArguments):
                await ctx.send(f"Too many arguments. Usage: {Triangulate().usage}")
        else:
            await ctx.send(f"Something unexpected happened {error}")
    
    @commands.command(name="tri_animate", description="create an animated triangulation of an image")
    async def tri_animation(self, ctx, *args):
        await ctx.send("Processing animation...")
        await process_command(ctx, TriAnimation(), *args)

    
    @tri_animation.error
    async def tri_animate_error_handler(self, ctx, error):
        if isinstance(error, (MissingRequiredArgument, TooManyArguments)):
            await ctx.send(f"Usage: {TriAnimation().usage}")
        elif isinstance(error, BadArgument):
            await ctx.send(error)
        elif isinstance(error, CommandInvokeError):
            if isinstance(error.__cause__, InvalidURL):
                await ctx.send(error.__cause__)
            elif isinstance(error.__cause__, TooManyArguments):
                await ctx.send(f"Too many arguments. Usage: {TriAnimation().usage}")
        else:
            await ctx.send(f"Something unexpected happened {error}")
    
    @commands.command(name="voronoi", description="create a voronoi diagram from an image")
    async def voronoi(self, ctx, points, seed, *args):
        await process_command(ctx, Voronoi(), *args, points=points, seed=seed)
    
    @voronoi.error
    async def voronoi_error_handler(self, ctx, error):
        if isinstance(error, (MissingRequiredArgument, TooManyArguments)):
            await ctx.send(f"Usage: {Voronoi().usage}")
        elif isinstance(error, BadArgument):
            await ctx.send(error)
        elif isinstance(error, CommandInvokeError):
            if isinstance(error.__cause__, InvalidURL):
                await ctx.send(error.__cause__)
            elif isinstance(error.__cause__, TooManyArguments):
                await ctx.send(f"Too many arguments. Usage: {Voronoi().usage}")
        else:
            await ctx.send(f"Something unexpected happened {error}")

    @commands.command(name="voronoi_animate", description="create an animated voronoi effect of an image")
    async def voronoi_animation(self, ctx, seed, *args):
        await ctx.send("Processing animation...")
        await process_command(ctx, VoronoiAnimation(), *args, seed=seed)

    @voronoi_animation.error
    async def voronoi_animate_error_handler(self, ctx, error):
        if isinstance(error, (MissingRequiredArgument, TooManyArguments)):
            await ctx.send(f"Usage: {VoronoiAnimation().usage}")
        elif isinstance(error, BadArgument):
            await ctx.send(error)
        elif isinstance(error, CommandInvokeError):
            if isinstance(error.__cause__, InvalidURL):
                await ctx.send(error.__cause__)
            elif isinstance(error.__cause__, TooManyArguments):
                await ctx.send(f"Too many arguments. Usage: {VoronoiAnimation().usage}")
        else:
            await ctx.send(f"Something unexpected happened {error}")
    
async def setup(bot):
    await bot.add_cog(EffectCog(bot))