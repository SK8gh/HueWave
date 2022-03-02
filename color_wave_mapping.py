import matplotlib.pyplot as plt
from colorthief import ColorThief
import config as config
import pandas as pd
import numpy as np
import cv2


class ColorWave:
    def __init__(self, img):
        self.colors_rgb = pd.read_csv("colors.csv", names=["color_name", "name_drop", "code", "R", "G", "B"])
        self.colors_rgb = self.colors_rgb.drop(["name_drop", "code"], axis=1)

        self.colors = config.colors
        self.img = img

        print(self.colors_rgb)

    def get_color_palette(self, nb_colors):
        """
        getting the main colors in self.img using the ColorThief class
        :param nb_colors:
        :return: palette (list of tuples)
        """
        color_thief = ColorThief(self.img)
        palette = color_thief.get_palette(color_count=nb_colors)
        return palette

    def distance_img_palette(self, palette_color):
        """
        implementing a distance metric between an image and a (r,g,b) vector
        :param palette_color:
        :return: distance value
        """
        len_csv = len(self.colors_rgb)
        distances = np.zeros([len_csv])

        for k in range(len_csv):
            p1, p2, p3 = palette_color
            r, g, b = self.colors_rgb[["R", "G", "B"]].iloc[k]

            distances[k] = abs(p1 - r) + abs(p2 - g) + abs(p3 - b)
        self.colors_rgb["color_presence"] = 100 / distances

    def get_colors(self):
        self.colors_rgb = self.colors_rgb.sort_values("color_presence")
        print(self.colors_rgb[["color_name"]].tail(10))

    def map_colors(self):
        pass


C = ColorWave("sverige.jpg")

palette_colors = C.get_color_palette(10)

C.distance_img_palette(palette_colors[0])

C.get_colors()



















