from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics.texture import Texture
from kivy.clock import Clock
import time
import cv2
import numpy as np
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import ObjectProperty
import matplotlib.pyplot as plt

from color_wave_mapping import ColorWave
from PIL import Image as ImagePil


class CameraPreview(Image):
    def __init__(self, **kwargs):
        super(CameraPreview, self).__init__(**kwargs)

        self.frame = None
        self.screenshot_path = "screenshot.jpg"
        self.capture = cv2.VideoCapture(0)

        Clock.schedule_interval(self.update, 2)

        # I didn't find a better method than saving the file (it'll be replaced for every image evaluation) and
        # opening it afterwards using ImagePil

    def update(self, dt):
        ret, self.frame = self.capture.read()
        buf = cv2.flip(self.frame, 0).tostring()
        texture = Texture.create(size=(self.frame.shape[1], self.frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.texture = texture

        screenshot = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        img = ImagePil.fromarray(np.array(screenshot), "RGB")
        img.save(self.screenshot_path)

        chord = ColorWave(self.screenshot_path).process_mapping(print_detected_colors=True)
        print(f"chord : {chord}")


class MyCameraApp(App):
    def build(self):
        return CameraPreview()


if __name__ == '__main__':
    MyCameraApp().run()


