from colorthief import ColorThief
import config as config
from PIL import Image
import pandas as pd
import numpy as np


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

    def _get_color_palette(self, nb_colors=2):
        """
        getting the main colors in self.img using the ColorThief class
        :param nb_colors:
        :return: palette (list of tuples)
        """
        color_thief = ColorThief(self.img)
        return color_thief.get_palette()

    def _distance_img_palette_color(self, palette_color):
        """
        implementing a distance metric between an image and a (r,g,b) vector
        :param palette_color:
        :return: distance value
        """
        palette_color = palette_color[:2]
        len_csv = len(self.colors_rgb)

        for p, p_color in enumerate(palette_color):
            distances = np.zeros([len_csv])
            for k, line in enumerate(self.colors_rgb.itertuples()):
                p1, p2, p3 = p_color
                r, g, b = line.R, line.G, line.B

                distances[k] = abs(p1 - r) + abs(p2 - g) + abs(p3 - b)
            self.colors_rgb["color_presence_" + str(p)] = 100 / distances

    def _get_colors(self, tail_factor=3):
        """
        getting the 2 (max) most present colors
        :param tail_factor:
        :return:
        """
        top_colors_vals = []
        df_cols = self.colors_rgb.columns

        for column in df_cols:
            if "color_presence" not in column:
                continue
            self.colors_rgb = self.colors_rgb.sort_values(column)
            top_colors_vals.extend(self.colors_rgb[["color_name"]].tail(tail_factor).values)

        # Making the list cleaner
        top_colors = [color_val[0] for color_val in top_colors_vals]

        # colors in the config are less elaborate than the ones in colors.csv thus we have to refine the top_colors list
        top_config_colors = []
        for color_str in config.colors:
            for top_color in top_colors:
                if color_str in top_color:
                    top_config_colors.append(color_str)
        return list(set(top_config_colors))[:2]

    def _get_chord(self, top_colors):
        """
        get chord associated to the top_colors list
        :param top_colors:
        :return:
        """
        if len(top_colors) > 3:
            raise ValueError(f"top_colors : {top_colors} must have length < 3")

        elif len(top_colors) == 1:
            return self.color_chords[top_colors[0]]

        elif len(top_colors) == 2:
            try:
                str_request = top_colors[0] + "&" + top_colors[1]
                return self.color_chords[str_request]
            except KeyError:
                try:
                    str_request = top_colors[1] + "&" + top_colors[0]
                    return self.color_chords[str_request]
                except KeyError:
                    return

    def process_mapping(self, print_detected_colors=False):
        """
        provided with a self object containing an image at initialization, this method returns the associated chord
        :return:
        """
        # getting palette using ColorThief
        palette_colors = self._get_color_palette()

        # getting distances
        self._distance_img_palette_color(palette_colors)

        # detecting top colors in the image
        detected_top_colors = self._get_colors()

        if print_detected_colors:
            print(f"detected colors : {detected_top_colors}")

        # returning chords using the determined mapping
        result_chords = self._get_chord(detected_top_colors)

        return result_chords
