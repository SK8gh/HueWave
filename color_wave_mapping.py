import matplotlib.pyplot as plt
import config as config
import pandas as pd
import numpy as np
import cv2


class ColorWave:
    """
    docstring
    """

    def __init__(self, img):
        self.colors_rgb = pd.read_csv("colors.csv", names=["color_name", "name_drop", "code", "R", "G", "B"])
        self.colors_rgb = self.colors_rgb.drop(["name_drop", "code"], axis=1)

        self.colors = config.colors
        self.img = img

    def distance_img_color(self, rgb_color):
        """
        implementing a distance metric between an image and a (r,g,b) vector
        :return: distance value
        """
        if not len(rgb_color) == 3:
            raise Exception(f"rgb_color argument must have length 3 but has length {len(rgb_color)}")

        img, img_shape = self.img, self.img.shape
        red, blue, green = rgb_color

        return 0
        dist = np.dot(self.img, rgb_color)

        return dist

    def get_colors(self):
        pass

    def map_colors(self):
        pass


img_test = cv2.imread("sverige.jpg")

print(f"shape = {img_test.shape}")

CW = ColorWave(img_test)

CW.colors_rgb["color_presence"] = np.zeros([len(CW.colors_rgb)])

for k, row in enumerate(CW.colors_rgb[["R", "G", "B"]].itertuples()):
    r, g, b = row.R, row.G, row.B

    distance = CW.distance_img_color((r, g, b))

    CW.colors_rgb.loc[k, "color_presence"] = distance

    CW.colors_rgb = CW.colors_rgb.sort_values("color_presence")

print(CW.colors_rgb.tail(10))

