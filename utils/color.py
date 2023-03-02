import cv2

"""Converts an image into grayscale"""
def grayscale(img_path):
    img = cv2.imread(img_path, 0)
    cv2.imwrite(img_path, img)