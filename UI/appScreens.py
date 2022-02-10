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
            self.company_logo = Image(source="Logo_White_A.png",
                                     pos_hint={"center_x": 0.5, "top": 0})
            self.window.add_widget(self.company_logo)

            self.system_logo = Image(source="DextraManus_White.png",
                                     size_hint=(0.5, 0.5),
                                     pos_hint={"center_x": 0.5, "center_y": 0.3},
                                     )
            self.window.add_widget(self.system_logo)

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
        #self.layout.spacing = 10
        self.layout.padding = [0, 10, 0, 10]

        self.system_logo = Image(source="DextraManus_White.png",
                                     pos_hint={"center_x": 0.5, "top": 0})
        self.system_logo.size_hint = (0.6, 0.4)
        self.layout.add_widget(self.system_logo)

        self.title = Label(text="Main Menu",
                           font_size=36,
                           bold=True,
                           color="#c3c3c3")
        self.title.size_hint = (0.6, 0.2)
        self.title.pos_hint = {"center_x": 0.5}
        self.layout.add_widget(self.title)

        self.buttonBox = BoxLayout(orientation='vertical')
        self.buttonBox.size_hint = (0.2, 0.3) # width, height
        self.buttonBox.pos_hint = {"center_x": 0.5} # center on screen
        self.layout.add_widget(self.buttonBox)

        self.btn_start = Button(
            text="",
            background_normal = 'buttons/Start.png',
            background_down = 'buttons/Start_Pressed.png'
        )

        self.btn_model = Button(
            text="",
            background_normal = 'buttons/Settings.png',
            background_down = 'buttons/Settings_Pressed.png'
        )

        self.btn_changePass = Button(
            text="",
            background_normal = 'buttons/Password.png',
            background_down = 'buttons/Password_Pressed.png'
        )
        
        self.buttonBox.add_widget(self.btn_start)

        self.btn_start.bind(on_press=self.go_to_tracking)
        self.btn_changePass.bind(on_press=self.goToChangePass)

        self.buttonBox.add_widget(self.btn_model)
        self.buttonBox.add_widget(self.btn_changePass)

        self.add_widget(self.layout)

        self.group_logo = Image(source="Logo_White_A.png",
                                     pos_hint={"center_x": 0.95, "bottom": 0})
        self.group_logo.size_hint = (None, 0.2)
        self.layout.add_widget(self.group_logo)



    def go_to_tracking(self, *args):
        self.manager.current = 'tracking'

    def goToChangePass(self, *args):
        self.manager.current = 'changepass'

class TrackingWindow(Screen):
    def __init__(self, **kwargs):
        super(TrackingWindow, self).__init__(**kwargs)
        self.calibration_step = True
        self.calibration_counter = 5

        self.calibration_phase = 0
        #0 = calibration incomplete and needs to be done
        #1 = calibration has started
        #2 = calibration complete, begin tracking
        #-1 = calibration error, reset

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
        self.callibrate_btn.bind(on_press=self.beginTracking)


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
                                      font_size=18,
                                      pos_hint={'center_x': 0.5},
                                      size_hint=(None, 0.1))
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
        # if self.check:
        #     self.tracking_window.add_widget(self.capture)
        #     self.check = False

        files = glob.glob('captures/*')
        for f in files:
            os.remove(f)

        Clock.schedule_interval(self.beginTracking, 1/10)
        self.calibration_event = Clock.schedule_interval(self.updateCalibrationCount, 1)

    def updateCalibrationCount(self, *args):
        self.calibration_counter -= 1

        if self.calibration_counter < 0:
            self.calibration_step = False
            self.calibration_phase = 2

    def beginTracking(self, *args):
        #self.tracking_window.remove_widget(self.tracking_prompts)

        if self.check:
            self.tracking_window.add_widget(self.capture)
            self.check = False

        self.ret, self.frame = self.vid.read()
        self.frame = cv2.flip(self.frame, 1)

        if self.calibration_phase == 0:
            #self.tracking_window.add_widget(self.capture)
            self.tracking_prompts.text = "Place hand in front of webcam to begin"

            self.calibration_phase = 1
            self.calibration_counter = 5
            self.beginSchedule()


        if self.calibration_phase == 1:
            calibration_passed = cvTools.checkHandTrack(self.frame)
            self.frame = cvTools.calibrationStep(self.frame, self.calibration_counter)

            if not calibration_passed:
                self.calibration_event.cancel()
                self.tracking_prompts.text = "Place right hand on screen as indicated for 5 seconds to begin"
                self.calibration_phase = -1

        
        if self.calibration_phase == -1:
            calibration_passed = cvTools.checkHandTrack(self.frame)

            if calibration_passed:
                self.calibration_counter = 5
                self.calibration_event = Clock.schedule_interval(self.updateCalibrationCount, 1)
                self.calibration_phase = 1


        if self.calibration_phase != 2:
            self.frame = cvTools.addHandOverlay(self.frame)

        old_name = 'captures/' + str(self.counter) + ".png"
        cv2.imwrite(old_name, self.frame)
        self.counter = self.counter + 1
        new_name = 'captures/' + str(self.counter) + '.png'
        os.rename(old_name, new_name)
        self.capture.source = new_name

    def goToMain(self, *args):
        self.calibration_counter = 5
        self.calibration_phase = 0
        self.manager.current = 'main'


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
            
class PasswordWindow(Screen):
        def __init__(self, **kwargs):
            super(PasswordWindow, self).__init__(**kwargs)

            self.layout = BoxLayout(orientation='vertical')
            self.layout.padding = [0, 10, 0, 10]

            self.system_logo = Image(source="DextraManus_White.png",
                                     pos_hint={"center_x": 0.5, "top": 0})
            self.system_logo.size_hint = (0.6, 0.3)
            self.layout.add_widget(self.system_logo)

            self.title = Label(text="Change Password",
                            font_size=36,
                            bold=True,
                            color="#c3c3c3")
            self.title.size_hint = (0.6, 0.2)
            self.title.pos_hint = {"center_x": 0.5}
            self.layout.add_widget(self.title)

            self.interaction_region = BoxLayout(orientation='horizontal')
            self.interaction_region.size_hint = (0.5, 0.5)
            self.interaction_region.pos_hint = {"center_x": 0.5}

            self.left_pane = BoxLayout(orientation='vertical')
            self.old_pass_prompt = Label(
                text="Enter Old Password *",
                font_size=18,
                color="#c3c3c3",
                halign="left"
            )
            self.old_pass_prompt.bind(size=self.old_pass_prompt.setter('text_size')) 
            self.left_pane.add_widget(self.old_pass_prompt)
            

            self.old_pass_field = TextInput(multiline=False,
                                        padding_y=(5,5),
                                        font_size=18,
                                        password=True,
                                        background_color=(48/255,51/255,57/255,1),
                                        foreground_color=(195/255, 195/255, 195/255, 1),
                                        size_hint=(0.6, 0.3)
                                        )
            self.left_pane.add_widget(self.old_pass_field)

            self.new_pass_prompt = Label(
                text="Enter New Password *",
                font_size=18,
                color="#c3c3c3"
            )
            self.new_pass_prompt.bind(size=self.new_pass_prompt.setter('text_size')) 
            self.left_pane.add_widget(self.new_pass_prompt)

            self.new_pass_field = TextInput(multiline=False,
                                        padding_y=(5,5),
                                        font_size=18,
                                        password=True,
                                        background_color=(48/255,51/255,57/255,1),
                                        foreground_color=(195/255, 195/255, 195/255, 1),
                                        size_hint=(0.6, 0.3)
                                        )
            self.left_pane.add_widget(self.new_pass_field)

            self.new_pass_ver_prompt = Label(
                text="Confirm New Password *",
                font_size=18,
                color="#c3c3c3"
            )
            self.new_pass_ver_prompt.bind(size=self.new_pass_ver_prompt.setter('text_size')) 
            self.left_pane.add_widget(self.new_pass_ver_prompt)

            self.new_pass_ver = TextInput(multiline=False,
                                        padding_y=(5,5),
                                        font_size=18,
                                        password=True,
                                        background_color=(48/255,51/255,57/255,1),
                                        foreground_color=(195/255, 195/255, 195/255, 1),
                                        size_hint=(0.6, 0.3)
                                        )
            self.left_pane.add_widget(self.new_pass_ver)



            self.right_pane = BoxLayout(orientation='vertical')
            self.pass_requirements = Label(
                text="Password Requirements:\n \u2022 At least 6 characters\n \u2022 Upper/lower case letters\n \u2022 Number or punctuation",
                font_size=18,
                color="#c3c3c3"
            )
            self.pass_requirements.bind(size=self.pass_requirements.setter('text_size')) 
            self.right_pane.add_widget(self.pass_requirements)
            self.right_pane.spacing = 10

            self.btn_apply = Button(
                text="",
                background_normal = 'buttons/ApplyChanges.png',
                background_down = 'buttons/ApplyChanges_Pressed.png'
            )
            self.btn_apply.size_hint = (0.4, 0.4)
            self.btn_apply.pos_hint = {"center_x": 0.25}
            self.right_pane.add_widget(self.btn_apply)


            self.btn_cancel = Button(
                text="",
                background_normal = 'buttons/Cancel.png',
                background_down = 'buttons/Cancel_Pressed.png'
            )
            self.btn_cancel.size_hint = (0.4, 0.4)
            self.btn_cancel.pos_hint = {"center_x": 0.25}
            self.right_pane.add_widget(self.btn_cancel)
            



            self.interaction_region.add_widget(self.left_pane)
            self.interaction_region.add_widget(self.right_pane)

            self.layout.add_widget(self.interaction_region)

            self.group_logo = Image(source="Logo_White_A.png",
                                     pos_hint={"center_x": 0.95, "bottom": 0})
            self.group_logo.size_hint = (None, 0.2)
            self.layout.add_widget(self.group_logo)


            self.add_widget(self.layout)