import cv2
import image_utils
from discord.ext import commands

"""draws black line between given points"""
async def drawline(img_path, start, stop, width):
    # print(start, stop, width)
    try:
        p1 = (int(start[0]), int(start[1]))
        p2 = (int(stop[0]), int(stop[1]))
        width = int(width)
    except:
        image_utils.delete_img(img_path)
        raise commands.UserInputError

    if (width <= 0):
        image_utils.delete_img(img_path)
        raise commands.BadArgument
    
    img = cv2.imread(img_path)
    cv2.line(img, p1, p2, (0, 0, 0), width)
    cv2.imwrite(img_path, img)
