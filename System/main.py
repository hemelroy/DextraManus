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

PASS = "123"

class DextraManusApp(App):
    def build(self):
        self.icon = "images/Logo_White_A_Cropped.png"
        wm = WindowManager(transition=FadeTransition())
        wm.add_widget(LoginWindow(name='login'))
        wm.add_widget(MainWindow(name='main'))
        wm.add_widget(TrackingWindow(name='tracking'))
        wm.add_widget(PasswordWindow(name='changepass'))
        wm.add_widget(ModelSettingsWindow(name='modelparams'))
        return wm

if __name__ == "__main__":
    Window.left = 0
    Window.top = 30
    Window.clearcolor = (54/255, 57/255, 63/255, 1)
    Window.background_color = (54/255, 57/255, 63/255, 1)
    Window.background_normal = ""
    Window.maximize()

    DextraManusApp().run()