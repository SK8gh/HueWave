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

from color_wave_mapping import ColorWave, ImageCT
from PIL import Image as ImagePil

class CameraPreview(Image):
    def __init__(self, **kwargs):
        super(CameraPreview, self).__init__(**kwargs)

        self.frame = None
        self.capture = cv2.VideoCapture(0)

        time.sleep(1)
        screenshot = self.update("")

        screenshot_ct = np.array(screenshot)

        screenshot_ct = ImagePil.fromarray(screenshot_ct)
        chord = ColorWave(screenshot_ct).process_mapping(print_detected_colors=True)
        print(chord)

    def update(self, dt):
        ret, self.frame = self.capture.read()
        buf = cv2.flip(self.frame, 0).tostring()
        texture = Texture.create(size=(self.frame.shape[1], self.frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.texture = texture

        return self.frame


class MyCameraApp(App):
    def build(self):
        return CameraPreview()


if __name__ == '__main__':
    MyCameraApp().run()


