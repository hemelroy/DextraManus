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
from kivy.uix.camera import Camera
from kivy.clock import Clock

import cv2
import cvTools
import numpy as np
import time
from threading import *
import os 
import glob


PASS = "123"

class WindowManager(ScreenManager):
    def __init__(self, **kwargs):
        super(WindowManager, self).__init__(**kwargs)

class LoginWindow(Screen):
        def __init__(self, **kwargs):
            super(LoginWindow, self).__init__(**kwargs)

            self.window = BoxLayout(orientation='vertical') #GridLayout()
            #self.window.cols = 1
            #self.window.rows = 
            self.window.size_hint = (0.5, 0.9)
            self.window.pos_hint = {"center_x": 0.5, "center_y": 0.5}
            self.window.spacing = 10

            #image widget
            self.system_logo = Image(source="logo-social.png",
                                     pos_hint={"center_x": 0.5, "top": 0})
            self.window.add_widget(self.system_logo)

            self.company_logo = Image(source="logo-social.png",
                                     size_hint=(0.5, 0.5),
                                     pos_hint={"center_x": 0.5, "center_y": 0.3},
                                     )
            self.window.add_widget(self.company_logo)

            self.password_prompt = Label(text="Machine Password",
                                         color="#c3c3c3",
                                         pos_hint = {"center_x": 0.5, "center_y": 0.5},
                                         font_size=28,
                                         bold=True,
                                         size_hint=(None, 0.2),
                                         )
            self.window.add_widget(self.password_prompt)

            #text input widget
            self.pass_field = TextInput(multiline=False,
                                        padding_y=(5,5),
                                        size_hint=(0.5, 0.2), #width, height
                                        #width=self.window.width,
                                        font_size=28,
                                        password=True,
                                        background_color=(48/255,51/255,57/255,1),
                                        foreground_color=(195/255, 195/255, 195/255, 1),
                                        pos_hint= {"center_x": 0.5, "center_y": 0.5},
                                        )
            self.window.add_widget(self.pass_field)

            self.auth_btn = Button(text="",
                                size_hint=(0.15, None),
                                bold=True,
                                background_normal = 'buttons/Run.png',
                                background_down = 'buttons/Run_Pressed.png',
                                #background_color=(63/255,72/255,204/255,1),
                                #background_normal="",
                                pos_hint= {"center_x": 0.5, "center_y": 0.5},
                                height=50)
            self.auth_btn.bind(on_press=self.authenticate)
            self.window.add_widget(self.auth_btn)

            self.add_widget(self.window)

            #label widget
            self.text_prompt = Label(text="",
                                    font_size=18,
                                    color="#c3c3c3")
            self.window.add_widget(self.text_prompt)

            # self.btn2 = Button(text='Go')
            # self.add_widget(self.btn2)
            # self.btn2.bind(on_press = self.screen_transition)

        def authenticate(self, *args):
            if self.pass_field.text == PASS:
                self.manager.current = 'main'
            else:
                self.text_prompt.text = "Incorrect password"

class MainWindow(Screen):
    #model settings, change password, start tracking, 
    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)

        self.layout = BoxLayout(orientation='vertical')
        
        self.btn_start = Button(
            text="Start Hand Tracking"
        )

        self.btn_model = Button(
            text="Model Settings"
        )

        self.btn_changePass = Button(
            text="Change Password"
        )
        
        self.layout.add_widget(self.btn_start)

        self.btn_start.bind(on_press=self.go_to_tracking)

        self.layout.add_widget(self.btn_model)
        self.layout.add_widget(self.btn_changePass)

        self.add_widget(self.layout)

    def go_to_tracking(self, *args):
            self.manager.current = 'tracking'

class TrackingWindow(Screen):
    def __init__(self, **kwargs):
        super(TrackingWindow, self).__init__(**kwargs)

        self.main_window = BoxLayout(orientation='horizontal')
        self.tracking_window = BoxLayout(orientation='vertical')
        self.status_window = FloatLayout() #BoxLayout(orientation='vertical')

        self.tracking_window.size_hint = (0.75, 0.9)
        self.status_window.size_hint = (0.25, 0.9)



        self.status_prompt = Label(text="Status:",
                                   color="#c3c3c3",
                                   font_size=28,
                                   bold=True,
                                   #size_hint=(0.5,0.1),
                                   pos_hint={'center_x': 0.5, 'center_y':0.9})
        self.status_window.add_widget(self.status_prompt)

        self.status_indicator = Label(text="Inactive", 
                                      color="red",
                                      font_size=24,
                                      pos_hint={'center_x': 0.5, 'center_y':0.85})
        self.status_window.add_widget(self.status_indicator)



        self.arduino_prompt = Label(text="Arduino:",
                                   color="#c3c3c3",
                                   font_size=28,
                                   bold=True,
                                   pos_hint={'center_x': 0.5, 'center_y':0.75})
        self.status_window.add_widget(self.arduino_prompt)

        self.arduino_indicator = Label(text="Disconnected", 
                                      color="red",
                                      font_size=24,
                                      pos_hint={'center_x': 0.5, 'center_y':0.7})
        self.status_window.add_widget(self.arduino_indicator)


        self.hand_prompt = Label(text="Hand Detected:",
                                   color="#c3c3c3",
                                   font_size=28,
                                   bold=True,
                                   pos_hint={'center_x': 0.5, 'center_y':0.6})
        self.status_window.add_widget(self.hand_prompt)

        self.hand_indicator = Label(text="None", 
                                      color="red",
                                      font_size=24,
                                      pos_hint={'center_x': 0.5, 'center_y':0.55})
        self.status_window.add_widget(self.hand_indicator)



        self.callibrate_btn = Button(text="",
                                     size_hint=(0.5, None),
                                     bold=True,
                                     #background_color=(63/255,72/255,204/255,1),
                                     #background_normal="",
                                     background_normal = 'buttons/Callibrate.png',
                                     background_down = 'buttons/Callibrate_Pressed.png',
                                     #height=50,
                                     pos_hint={'center_x': 0.5, 'center_y':0.45})
        self.status_window.add_widget(self.callibrate_btn)
        self.callibrate_btn.bind(on_press=self.beginSchedule)


        self.exit_btn = Button(text="",
                                     size_hint=(0.5, None),
                                     bold=True,
                                     #background_color=(1,0,0,1),
                                     #background_normal="",
                                     #height=50,
                                     background_normal = 'buttons/Exit.png',
                                     background_down = 'buttons/Exit_Pressed.png',
                                     pos_hint={'center_x': 0.5, 'center_y':0.3})
        self.status_window.add_widget(self.exit_btn)



        self.tracking_prompts = Label(text="Press calibrate to begin",
                                      font_size=24,
                                      pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.tracking_window.add_widget(self.tracking_prompts)




        self.main_window.add_widget(self.tracking_window)
        self.main_window.add_widget(self.status_window)
        self.add_widget(self.main_window)

        self.check = True
        self.capture = Image()
        self.vid = cv2.VideoCapture(0)
        self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        #self.ret, self.frame = self.vid.read()
        self.counter = 0


    def beginSchedule(self, *args):
        if self.check:
            self.tracking_window.add_widget(self.capture)
            self.check = False

        files = glob.glob('captures/*')
        for f in files:
            os.remove(f)

        Clock.schedule_interval(self.beginTracking, 1/30)

    def beginTracking(self, *args):
        self.tracking_window.remove_widget(self.tracking_prompts)

        # self.capture = Camera(resolution=(1280, 720))
        # self.tracking_window.add_widget(self.capture)

        # height, width = self.capture.texture.height, self.capture.texture.width
        # newvalue = np.frombuffer(self.capture.texture.pixels, np.uint8)
        # newvalue = newvalue.reshape(height, width, 4)
        # cv2.imwrite("test.png", newvalue)

        #self.capture.source = "input2.png"

        # T = Thread(target = self.showWebcam)
        # # change T to daemon
        # T.setDaemon(True)                  
        # # starting of Thread T
        # T.start()       

        self.ret, self.frame = self.vid.read()
        old_name = 'captures/' + str(self.counter) + ".png"
        cv2.imwrite(old_name, self.frame)
        self.counter = self.counter + 1
        new_name = 'captures/' + str(self.counter) + '.png'
        os.rename(old_name, new_name)
        self.capture.source = new_name

    # def update(self, dt):
    #     # display image from cam in opencv window
    #     ret, frame = self.capture.read()
    #     #cv2.imshow("CV2 Image", frame)
    #     # convert it to texture
    #     buf1 = cv2.flip(frame, 0)
    #     buf = buf1.tostring()
    #     texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr') 
    #     #if working on RASPBERRY PI, use colorfmt='rgba' here instead, but stick with "bgr" in blit_buffer. 
    #     texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
    #     # display image from the texture
    #     self.img1.texture = texture1


    def showWebcam(self, *args):
        vid = cv2.VideoCapture(0)
        counter = 0

        while(True):
            ret, frame = vid.read()

            if counter:
                cv2.imwrite("input3.png", frame)
                self.capture.source = "input3.png"
                counter = 0
            else:
                counter = 1
                cv2.imwrite("input2.png", frame)
                self.capture.source = "input2.png" 
            

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        vid.release()
            
