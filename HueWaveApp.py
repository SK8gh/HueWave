from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput


class HueWave(App):
    """
    HW Application
    """
    def __init__(self):
        super().__init__()
        self.window = GridLayout()

    def build(self):
        self.window.cols = 1

        self.window.add_widget(Image(source="sverige.jpg"))

        return self.window

# chord = ColorWave("sverige.jpg").process_mapping()
# print(chord)
