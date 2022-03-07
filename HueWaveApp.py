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
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import ObjectProperty

from color_wave_mapping import ColorWave


class ImageButton(ButtonBehavior, Image):
    preview = ObjectProperty(None)

    def on_press(self):
        cv2.namedWindow("CV2 Image")
        cv2.imshow("CV2 Image", self.preview.frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


class CameraPreview(Image):
    def __init__(self, **kwargs):
        super(CameraPreview, self).__init__(**kwargs)

        self.frame = None
        self.capture = cv2.VideoCapture(0)

        Clock.schedule_interval(self.update, 1.0 / 30)

    def update(self, dt):
        ret, self.frame = self.capture.read()
        buf = cv2.flip(self.frame, 0).tostring()
        texture = Texture.create(size=(self.frame.shape[1], self.frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        print(self.frame)
        self.texture = texture


class MyCameraApp(App):
    def build(self):
        return CameraPreview()


if __name__ == '__main__':
    MyCameraApp().run()


