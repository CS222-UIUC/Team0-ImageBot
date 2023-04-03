import cv2
import image_utils
import os
import numpy as np
from discord.ext import commands


curr_color = (0, 0, 0)
SWATCH_SIZE = 100

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
    # print(curr_color)
    img = cv2.imread(img_path)
    cv2.line(img, p1, p2, curr_color, width)
    cv2.imwrite(img_path, img)

"""draws rect bounded by two points"""
async def drawrect(img_path, start, stop, width):
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
    cv2.rectangle(img, p1, p2, curr_color, width)
    cv2.imwrite(img_path, img)

async def pick_color(ctx, color):
    global curr_color
    try:
        curr_color = (int(color[0])%256, int(color[1])%256, int(color[2])%256)
    except:
        raise commands.BadArgument
    # curr_color = color
    if not os.path.exists(image_utils.IMG_DIR):
        os.mkdir(image_utils.IMG_DIR)

    blank_image = np.zeros((SWATCH_SIZE, SWATCH_SIZE, 3), np.uint8)
    blank_image[:,:] = curr_color

    await image_utils.send_img_by_mat(ctx, blank_image, "swatch.jpg")

async def sample_color(img_path, n_colors):
    try:
        n_colors = int(n_colors)
    except:
        image_utils.delete_img(img_path)
        raise commands.BadArgument
    global curr_color
    img = cv2.imread(img_path)
    pixels = np.float32(img.reshape(-1, 3))

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
    flags = cv2.KMEANS_RANDOM_CENTERS

    _, labels, palette = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
    _, counts = np.unique(labels, return_counts=True)

    dominant = palette[np.argmax(counts)]
    curr_color = (int(dominant[0]), int(dominant[1]), int(dominant[2]))

    blank_image = np.zeros((SWATCH_SIZE, SWATCH_SIZE, 3), np.uint8)
    blank_image[:,:] = curr_color
    cv2.imwrite(img_path, blank_image)


