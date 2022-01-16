from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.lang import Builder
from kivy.core.window import Window

from appScreens import *

import ctypes

PASS = "123"

class TrackingApp(App):
    def build(self):
        wm = WindowManager(transition=FadeTransition())
        wm.add_widget(LoginWindow(name='login'))
        wm.add_widget(MainWindow(name='main'))
        wm.add_widget(TrackingWindow(name='tracking'))
        return wm

if __name__ == "__main__":
    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    Window.size = screensize
    Window.left = 0
    Window.top = 30
    Window.clearcolor = (54/255, 57/255, 63/255, 1)
    Window.background_color = (54/255, 57/255, 63/255, 1)
    Window.background_normal = ""

    #TODO: change to being auto maximized without setting default screen size to full
    TrackingApp().run()