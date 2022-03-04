from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
import time
from color_wave_mapping import ColorWave

Builder.load_string('''
<CameraClick>:
    orientation: 'vertical'
    Camera:
        id: camera
        resolution: (640, 480)
        play: True
    Button:
        text: 'Capture'
        size_hint_y: None
        height: '48dp'
        on_press: root.capture()
''')


class CameraClick(BoxLayout):
    def __init__(self, **kwargs):
        self.last_img_captured, self.last_chord = None, None
        super().__init__(**kwargs)

    def capture(self):
        """
        Function to capture the images and give them the names
        according to their captured time and date
        :return:
        """
        camera = self.ids['camera']
        time_str = time.strftime("%Y%m%d_%H%M%S")

        path_saved_img = "IMG_{}.png".format(time_str)

        d = dir(camera)

        # TODO: fix, do not export, just save in a variable
        camera.export_to_png(path_saved_img)
        print("click!")

        chord = ColorWave(path_saved_img).process_mapping()
        print(chord)


class HueWave(App):
    def build(self):
        return CameraClick()


HueWave().run()









