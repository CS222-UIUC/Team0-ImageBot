from discord.ext.commands import BadArgument

from triangler import *

from command import Command

class Triangulate(Command):
    MIN_POINTS = 1
    MAX_POINTS = 16383

    def __init__(self):
        super().__init__("$triangulate [points] [image link/uploaded image]")
    
    async def command(self, img_path, points: int):
        if points > self.MAX_POINTS or points < self.MIN_POINTS:
            raise BadArgument(f"Number of points must be in range [{self.MIN_POINTS}, {self.MAX_POINTS}]")
        triangler_instance = Triangler(
            edge_method=EdgeMethod.SOBEL,
            sample_method=SampleMethod.POISSON_DISK,
            color_method=ColorMethod.CENTROID,
            points=points,
            blur=2,
            pyramid_reduce=True,
        )
        triangler_instance.convert_and_save(img_path, img_path)