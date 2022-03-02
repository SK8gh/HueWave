import matplotlib.pyplot as plt
from colorthief import ColorThief
import config as config
import pandas as pd
import numpy as np
import cv2


class ColorWave:
    def __init__(self, img):
        """
        initializing the ColorWave class using an image
        :param img:
        """
        self.colors_rgb = pd.read_csv("colors.csv", names=["color_name", "name_drop", "code", "R", "G", "B"])
        self.colors_rgb = self.colors_rgb.drop(["name_drop", "code"], axis=1)

        self.color_chords = config.color_chords
        self.colors = config.colors
        self.img = img

    def get_color_palette(self, nb_colors=10):
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

    def get_colors(self, tail_factor=10):
        """
        getting the 2 (max) most present colors
        :param tail_factor:
        :return:
        """
        self.colors_rgb = self.colors_rgb.sort_values("color_presence")
        top_colors_vals = self.colors_rgb[["color_name"]].tail(tail_factor).values

        # Making the list cleaner
        top_colors = [color_val[0] for color_val in top_colors_vals]

        # colors in the config are less elaborate than the ones in colors.csv thus we have to refine the top_colors list
        top_config_colors = []
        for color_str in config.colors:
            for top_color in top_colors:
                if color_str in top_color:
                    top_config_colors.append(color_str)
        return list(set(top_config_colors))[:2]

    def get_chord(self, top_colors):
        """
        get chord associated to the top_colors list
        :param top_colors:
        :return:
        """
        if len(top_colors) == 1:
            return self.color_chords[top_colors]

        elif len(top_colors) == 2:
            str_request = top_colors[0] + "&" + top_colors[1]
            return self.color_chords[str_request]

        else:
            raise ValueError(f"top_colors : {top_colors} must have length < 3")

    def process_mapping(self):
        """
        provided with a self object containing an image at initialization, this method returns the associated chord
        :return:
        """
        # getting palette using ColorThief
        palette_colors = self.get_color_palette(10)

        # getting distances
        self.distance_img_palette(palette_colors[0])
        detected_colors = self.get_colors()

        chord = self.get_chord(detected_colors)
        return chord