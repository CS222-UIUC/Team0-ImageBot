import cv2
from command import Command

import image_utils
from discord.ext import commands


class Grayscale(Command):
    def __init__(self):
        super().__init__("$grayscale [image link/uploaded image]")

    """Converts an image into grayscale"""

    async def command(self, img_path):
        img = cv2.imread(img_path, 0)
        cv2.imwrite(img_path, img)
        return img_path


class Hue(Command):
    def __init__(self):
        super().__init__("$hue [change] [url]. Hue change is between 0 and 180.")

    async def command(self, img_path, change):
        img = cv2.imread(img_path)

        try:
            change = int(change)
        except ValueError:
            raise (commands.BadArgument("Invalid hue change."))

        if change < 0 or change > 180:
            raise (commands.BadArgument("Hue change is between 0 and 180."))

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h = hsv[:, :, 0]
        s = hsv[:, :, 1]
        v = hsv[:, :, 2]

        huechange = change  # 0 is no change; 0<=huechange<=180
        hnew = cv2.add(h, huechange)

        hsvnew = cv2.merge([hnew, s, v])

        result = cv2.cvtColor(hsvnew, cv2.COLOR_HSV2BGR)

        cv2.imwrite(img_path, result)
        return img_path
