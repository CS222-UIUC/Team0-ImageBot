import cv2
from command import Command

class Grayscale(Command):
    def __init__(self):
        super().__init__("$grayscale [image link/uploaded image]")

    """Converts an image into grayscale"""
    async def command(self, img_path):
        img = cv2.imread(img_path, 0)
        cv2.imwrite(img_path, img)