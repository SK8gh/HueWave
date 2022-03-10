from kivy.graphics.texture import Texture
from color_wave_mapping import ColorWave
from PIL import Image as ImagePil
from kivy.uix.image import Image
from playsound import playsound
from kivy.clock import Clock
from kivy.app import App
import config as config
import numpy as np
import cv2


class CameraPreview(Image):
    def __init__(self, **kwargs):
        super(CameraPreview, self).__init__(**kwargs)

        self._frame = None
        self._update_rate = 20  # camera view update rate (in seconds)
        self._screenshot_path = "screenshot.jpg"

        self.previous_chord = None
        self.capture = cv2.VideoCapture(0)

        # running the self.update function every self._update_rate seconds
        Clock.schedule_interval(self.update, self._update_rate)

    def play_chord(self):
        chord_value = self.previous_chord
        chord_mp3_path = config.chords_mp3_files[chord_value]
        playsound(chord_mp3_path)
        return

    def update(self, dt):
        """
        updating the camera view and changing the mapped chord if necessary
        :param dt:
        :return:
        """
        ret, self._frame = self.capture.read()
        buf = cv2.flip(self._frame, 0).tostring()
        texture = Texture.create(size=(self._frame.shape[1], self._frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.texture = texture

        screenshot = cv2.cvtColor(self._frame, cv2.COLOR_BGR2RGB)
        img = ImagePil.fromarray(np.array(screenshot), "RGB")
        img.save(self._screenshot_path)

        chord = ColorWave(self._screenshot_path).process_mapping(print_detected_colors=True)
        if chord != self.previous_chord:
            self.previous_chord = chord

            self.play_chord()


class MyCameraApp(App):
    def build(self):
        return CameraPreview()


if __name__ == '__main__':
    MyCameraApp().run()


