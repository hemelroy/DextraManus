from turtle import window_height
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
from kivy.core.window import Window
from kivy.uix.slider import Slider
from kivy.uix.togglebutton import ToggleButton

import cv2
import handTracking
import dataStorage
import numpy as np
import time
from threading import *
import os 
import glob

#import pythonSerial


PASS = "123"

class WindowManager(ScreenManager):
    def __init__(self, **kwargs):
        super(WindowManager, self).__init__(**kwargs)

class LoginWindow(Screen):
        def __init__(self, **kwargs):
            super(LoginWindow, self).__init__(**kwargs)

            ######################## Widgets ########################
            self.window = BoxLayout(orientation='vertical')
            self.window.size_hint = (0.6, 0.9)
            self.window.pos_hint = {"center_x": 0.5}
            self.window.spacing = 10
            current_width, current_height = Window.size

            self.combined_logo = Image(source="images/combined_logos.png",
                                       pos_hint={"center_x": 0.5},
                                       size_hint = (None, None),
                                       height = round(current_height/2.25),
                                       width = round(1.73*(current_height/2.25)))
            self.window.add_widget(self.combined_logo)

            self.password_prompt = Label(text="Machine Password",
                                         color="#c3c3c3",
                                         pos_hint = {"center_x": 0.5},
                                         font_size=28,
                                         bold=True)
            self.window.add_widget(self.password_prompt)

            self.pass_field = TextInput(multiline=False,
                                        padding_y=(5,5),
                                        size_hint=(None, None), #width, height
                                        font_size=28,
                                        password=True,
                                        background_color=(48/255,51/255,57/255,1),
                                        foreground_color=(195/255, 195/255, 195/255, 1),
                                        pos_hint= {"center_x": 0.5},
                                        width=current_width//4,
                                        height=current_height//20)
            self.window.add_widget(self.pass_field)

            self.auth_btn = Button(text="",
                                   size_hint=(None, None),
                                   bold=True,
                                   background_normal = 'buttons/Run.png',
                                   background_down = 'buttons/Run_Pressed.png',
                                   pos_hint= {"center_x": 0.5},
                                   height=50)
            self.auth_btn.bind(on_press=self.authenticate)
            self.window.add_widget(self.auth_btn)

            self.add_widget(self.window)

            self.text_prompt = Label(text="",
                                    font_size=18,
                                    color="#c3c3c3")
            self.window.add_widget(self.text_prompt)

        #Function that checks password against what is stored in the database
        def authenticate(self, *args):
            if self.pass_field.text == PASS:
                self.manager.current = 'main'
            else:
                self.text_prompt.text = "Incorrect password"

class MainWindow(Screen):
    #model settings, change password, start tracking, 
    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)

        ######################## Widgets ########################
        self.layout = BoxLayout(orientation='vertical')
        self.layout.spacing = 10
        self.layout.padding = [0, 10, 0, 10]
        current_width, current_height = Window.size

        self.system_logo = Image(source="images/DextraManus_White_Cropped.png",
                                 pos_hint={"center_x": 0.5, "top": 0.1})
        #self.system_logo.size_hint = (0.6, 0.4)
        self.layout.add_widget(self.system_logo)

        self.title = Label(text="Main Menu",
                           font_size=30,
                           bold=True,
                           color="#c3c3c3")
        #self.title.size_hint = (0.6, 0.2)
        self.title.pos_hint = {"center_x": 0.5}
        self.layout.add_widget(self.title)

        self.buttonBox = BoxLayout(orientation='vertical')
        #self.buttonBox.size_hint = (0.2, 0.3) # width, height
        self.buttonBox.pos_hint = {"center_x": 0.5} # center on screen
        self.buttonBox.spacing = 10
        self.layout.add_widget(self.buttonBox)

        self.btn_start = Button(text="",
                                background_normal = 'buttons/Start.png',
                                background_down = 'buttons/Start_Pressed.png',
                                size_hint=(None, None),
                                pos_hint = {"center_x": 0.5},
                                width=round(current_width/4.8),
                                height=round(current_height/9))

        self.btn_model = Button(text="",
                                background_normal = 'buttons/Settings.png',
                                background_down = 'buttons/Settings_Pressed.png',
                                size_hint=(None, None),
                                pos_hint = {"center_x": 0.5},
                                width=round(current_width/4.8),
                                height=round(current_height/9))

        self.btn_changePass = Button(text="",
                              background_normal = 'buttons/Password.png',
                              background_down = 'buttons/Password_Pressed.png',
                              size_hint=(None, None),
                              pos_hint = {"center_x": 0.5},
                              width=round(current_width/4.8),
                              height=round(current_height/9))
        
        self.buttonBox.add_widget(self.btn_start)

        self.btn_start.bind(on_press=self.goToTracking)
        self.btn_changePass.bind(on_press=self.goToChangePass)
        self.btn_model.bind(on_press=self.goToModelParams)

        self.buttonBox.add_widget(self.btn_model)
        self.buttonBox.add_widget(self.btn_changePass)
        self.add_widget(self.layout)

        self.group_logo = Image(source="images/Logo_White_A_Cropped.png",
                                pos_hint={"center_x": 0.95, "bottom": 0},
                                size_hint=(None, None),
                                width=round(current_width/18.46),
                                height=round(current_height/9.75))
        #self.group_logo.size_hint = (None, 0.2)
        self.layout.add_widget(self.group_logo)



    def goToTracking(self, *args):
        self.manager.current = 'tracking'

    def goToChangePass(self, *args):
        self.manager.current = 'changepass'

    def goToModelParams(self, *args):
        self.manager.current = 'modelparams'

class TrackingWindow(Screen):
    def __init__(self, **kwargs):
        super(TrackingWindow, self).__init__(**kwargs)
        #Create a model object loading values from settings
        self.stor = dataStorage.StorageManager("settings.db")
        #Get values for model parameters and use them to construct hand tracker object
        model_params = self.stor.getModelParams()
        self.hand_tracker = handTracking.HandTracker(model_params[0], model_params[1], model_params[2])


        #Calibration variables
        self.calibration_step = True
        self.calibration_counter = 5
        self.calibration_phase = 0
        #0 = calibration incomplete and needs to be done
        #1 = calibration has started
        #2 = calibration complete, begin tracking
        #-1 = calibration error, reset

        self.begin_transmit = False

        Window.bind(on_key_down=self._keydown)

        #Draw widgets to screen
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
        self.exit_btn.bind(on_press=self.terminateTracking)



        self.tracking_prompts = Label(text="Press calibrate to begin",
                                      font_size=18,
                                      pos_hint={'center_x': 0.5},
                                      size_hint=(None, 0.1))
        self.tracking_window.add_widget(self.tracking_prompts)




        self.main_window.add_widget(self.tracking_window)
        self.main_window.add_widget(self.status_window)
        self.add_widget(self.main_window)

        self.show_camera_cap = True #Add the widget for the first time to screen
        self.camera_open = True #Tracks whether camera object needs to be created or not
        self.capture = Image()
        self.vid = cv2.VideoCapture(0)
        self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        #self.ret, self.frame = self.vid.read()
        self.capture_counter = 0

    def beginSchedule(self, *args):
        # if self.check:
        #     self.tracking_window.add_widget(self.capture)
        #     self.check = False

        files = glob.glob('captures/*')
        for f in files:
            os.remove(f)

        self.tracking_event = Clock.schedule_interval(self.beginTracking, 1/10)
        self.calibration_event = Clock.schedule_interval(self.updateCalibrationCount, 1)

    def updateCalibrationCount(self, *args):
        self.calibration_counter -= 1

        if self.calibration_counter < 0:
            self.calibration_step = False
            self.calibration_phase = 2
            self.begin_transmit = True
            Clock.unschedule(self.calibration_event)

    def terminateTracking(self, *args):
        if self.calibration_phase != 0:
            Clock.unschedule(self.tracking_event, all=True)
            Clock.unschedule(self.calibration_event, all=True)
            #self.tracking_event.cancel()
            self.vid.release()
        #self.calibration_phase = 3
        self.tracking_window.remove_widget(self.capture)
        self.show_camera_cap = True
        self.calibration_phase = 0
        self.camera_open = False
        self.calibration_counter = 5
        self.calibration_step = True

        #Reset prompts
        self.tracking_prompts.text = "Press calibrate to begin"
        self.status_indicator.text = "Inactive"
        self.status_indicator.color = "red"
        self.hand_indicator.text = "None"
        self.hand_indicator.color = "red"

        self.manager.current = 'main'

    def transmitPosition(self, *args):
        data = self.hand_tracker.output

        isWorking = pythonSerial.transmit(data)

        if not isWorking:
            Clock.unschedule(self.transmit_event)
            self.tracking_prompts.text = "Transmission error"

    def _keydown(self,*args):
        key_char = args[-2]

        if key_char == " " and self.calibration_phase == 2:
            self.performEmergencyStop()
            #print("Space Pressed")

    def performEmergencyStop(self, *args):
        if self.calibration_phase != 0:
            Clock.unschedule(self.tracking_event, all=True)
            Clock.unschedule(self.calibration_event, all=True)
            self.vid.release()

        self.tracking_window.remove_widget(self.capture)
        self.show_camera_cap = True
        self.calibration_phase = 0
        self.camera_open = False
        self.calibration_counter = 5
        self.calibration_step = True
        self.tracking_prompts.text = "EMERGENCY STOP triggered. System has has stopped accepting input."

        self.status_indicator.text = "Inactive"
        self.status_indicator.color = "red"
        self.hand_indicator.text = "None"
        self.hand_indicator.color = "red"


    #Event when calibrate button is pressed
    def beginTracking(self, *args):
        #self.tracking_window.remove_widget(self.tracking_prompts)

        if not self.camera_open:
            self.vid = cv2.VideoCapture(0)
            self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            self.camera_open = True

        if self.show_camera_cap:
            self.tracking_window.add_widget(self.capture)
            self.show_camera_cap = False

        self.ret, self.frame = self.vid.read()
        self.frame = cv2.flip(self.frame, 1)

        if self.calibration_phase == 0:
            #self.tracking_window.add_widget(self.capture)
            self.tracking_prompts.text = "Place hand in front of webcam to begin"

            self.calibration_phase = 1
            self.calibration_counter = 5
            self.beginSchedule()


        if self.calibration_phase == 1:
            handedness = self.hand_tracker.checkHandTrack(self.frame)

            if handedness == "Right":
                calibration_passed = True
                self.hand_indicator.text = "Right"
                self.hand_indicator.color = "green"
            elif handedness == "Left":
                calibration_passed = False
                self.hand_indicator.text = "Left"
                self.hand_indicator.color = "red"
            else:
                calibration_passed = False
                self.hand_indicator.text = "None"
                self.hand_indicator.color = "red"

            self.frame = self.hand_tracker.calibrationStep(self.frame, self.calibration_counter)

            if not calibration_passed:
                #self.calibration_event.cancel()
                Clock.unschedule(self.calibration_event)
                self.tracking_prompts.text = "Place right hand on screen as indicated for 5 seconds to begin"
                self.calibration_phase = -1

        
        if self.calibration_phase == -1:
            handedness = self.hand_tracker.checkHandTrack(self.frame)

            if handedness == "Right":
                calibration_passed = True
                self.hand_indicator.text = "Right"
                self.hand_indicator.color = "green"
            elif handedness == "Left":
                calibration_passed = False
                self.hand_indicator.text = "Left"
                self.hand_indicator.color = "red"
            else:
                calibration_passed = False
                self.hand_indicator.text = "None"
                self.hand_indicator.color = "red"

            if calibration_passed:
                self.calibration_counter = 5
                self.calibration_event = Clock.schedule_interval(self.updateCalibrationCount, 1)
                self.calibration_phase = 1


        if self.calibration_phase != 2:
            self.frame = self.hand_tracker.addHandOverlay(self.frame)

        #In hand tracking phase
        if self.calibration_phase == 2:
            self.frame, hand_found = self.hand_tracker.performHandTracking(self.frame)
            self.tracking_prompts.text = "Press SPACE or remove hand from frame for emergecy stop"
            self.status_indicator.text = "Active"
            self.status_indicator.color = "green"

            if not hand_found:
                self.performEmergencyStop()

            if self.begin_transmit:
                #self.transmit_event = Clock.schedule_interval(self.transmitPosition, 2)
                print("---------------Scheduled Transmit Event----------------------")
                self.begin_transmit = False


        old_name = 'captures/' + str(self.capture_counter) + ".png"
        cv2.imwrite(old_name, self.frame)
        self.capture_counter = self.capture_counter + 1
        new_name = 'captures/' + str(self.capture_counter) + '.png'
        os.rename(old_name, new_name)
        self.capture.source = new_name


    def goToMain(self, *args):
        self.calibration_counter = 5
        self.calibration_phase = 0
        self.manager.current = 'main'


    def showWebcam(self, *args):
        #vid = cv2.VideoCapture(0)
        counter = 0

        while(True):
            ret, frame = self.vid.read()

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
                background_normal = 'buttons/Save.png',
                background_down = 'buttons/Save_Pressed.png'
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


class ModelSettingsWindow(Screen):
        def __init__(self, **kwargs):
            super(ModelSettingsWindow, self).__init__(**kwargs)

            self.model_store = dataStorage.StorageManager("settings.db")
            self.model_complexity, self.min_det_conf, self.min_track_conf = self.model_store.getModelParams()

            ######################## Widgets ########################
            current_width, current_height = Window.size
            self.parent_component = BoxLayout(orientation='vertical')
            self.parent_component.size_hint = (0.9, 0.9)
            self.add_widget(self.parent_component)
            self.system_logo = Image(source="images/DextraManus_White_Cropped.png",
                                     pos_hint={"center_x": 0.55, "top": 0.1})
            self.parent_component.add_widget(self.system_logo)

            self.title = Label(text="Model Parameters",
                               font_size=28,
                               bold=True,
                               color="#c3c3c3",
                               pos_hint={"center_x": 0.55})
            self.parent_component.add_widget(self.title)


            # self.layout = BoxLayout(orientation='vertical')
            # # self.layout.spacing = 10
            # # self.layout.padding = [0, 10, 0, 10]
            # current_width, current_height = Window.size

            # self.system_logo = Image(source="images/DextraManus_White_Cropped.png",
            #                          pos_hint={"center_x": 0.5, "top": 0.1})
            # self.layout.add_widget(self.system_logo)

            # self.title = Label(text="Model Parameters",
            #                    font_size=30,
            #                    bold=True,
            #                    color="#c3c3c3",)
            # self.title.pos_hint = {"center_x": 0.5, "top": 0.4}
            # self.layout.add_widget(self.title)

            # #self.det_conf_row = BoxLayout(orientation='horizontal')
            # #self.settings_grid = GridLayout(cols=2, row_force_default=True, row_default_height=40)
            # self.split_panes = BoxLayout(orientation='horizontal')
            # self.left_pane = BoxLayout(orientation='vertical')
            # self.right_pane = BoxLayout(orientation='vertical')
            # self.layout.add_widget(self.split_panes)
            # self.split_panes.add_widget(self.left_pane)
            # self.split_panes.add_widget(self.right_pane)


            # self.complexity_prompt = Label(text="Model Complexity",
            #                              font_size=18,
            #                              color="#c3c3c3",
            #                              )
            # self.left_pane.add_widget(self.complexity_prompt)

            # self.btn_group = BoxLayout(orientation='horizontal')
            # self.btn_group.height = 50
            # self.simple_btn = ToggleButton(text='Simple', group='complexity', state='down')
            # self.complex_btn = ToggleButton(text='Complex', group='complexity', state='normal')
            # self.btn_group.add_widget(self.simple_btn)
            # self.btn_group.add_widget(self.complex_btn)
            # self.right_pane.add_widget(self.btn_group)
            # self.left_pane.size_hint = (None, None)
            # self.left_pane.width = round(current_width / 2.5)
            # self.right_pane.size_hint = (None, None)
            # self.right_pane.width = round(current_width / 2.5)
            # self.left_pane.height = current_height // 2
            # self.right_pane.height = current_height//2

            # self.det_conf_prompt = Label(text="Min Detection Confidence",
            #                              font_size=18,
            #                              color="#c3c3c3",
            #                              )
            # self.left_pane.add_widget(self.det_conf_prompt)

            # self.slider_group1 = BoxLayout(orientation='horizontal')
            # self.det_conf_slider = Slider(min=0.5, 
            #                               max=1, 
            #                               value=float(self.min_det_conf), 
            #                               value_track=True, 
            #                               value_track_color=[1, 0, 0, 1],
            #                               size_hint=(None, None),
            #                               width=round(current_width/4),
            #                               )
            # self.slider_group1.add_widget(self.det_conf_slider)
            # self.det_conf_slider.bind(value=self.updateDetConfIndicator)

            # self.det_conf_indicator = Label(text=str(self.det_conf_slider.value),
            #                                 font_size=18,
            #                                 color="#c3c3c3",
            #                                 )
            # self.slider_group1.add_widget(self.det_conf_indicator)
            # self.right_pane.add_widget(self.slider_group1)

            

            # self.track_conf_prompt = Label(text="Min Tracking Confidence",
            #                              font_size=18,
            #                              color="#c3c3c3",
            #                              )
            # self.left_pane.add_widget(self.track_conf_prompt)

            # self.slider_group2 = BoxLayout(orientation='horizontal')
            # self.track_conf_slider = Slider(min=0.5, 
            #                               max=1, 
            #                               value=float(self.min_track_conf), 
            #                               value_track=True, 
            #                               value_track_color=[1, 0, 0, 1],
            #                               size_hint=(None, None),
            #                               width=round(current_width/4),
            #                               height=30,
            #                               )
            # self.slider_group2.add_widget(self.track_conf_slider)
            # self.track_conf_slider.bind(value=self.updateTrackConfIndicator)

            # self.track_conf_indicator = Label(text=str(self.track_conf_slider.value),
            #                                 font_size=18,
            #                                 color="#c3c3c3",
            #                                 )
            # self.slider_group2.add_widget(self.track_conf_indicator)
            # self.right_pane.add_widget(self.slider_group2)


            # self.return_buttons = BoxLayout(orientation="horizontal")
            # self.save_btn = Button(text="Save",
            #                        size_hint=(None, None),
            #                        bold=True,
            #                        #background_normal = 'buttons/Run.png',
            #                        #background_down = 'buttons/Run_Pressed.png',
            #                        #pos_hint= {"center_x": 0.5},
            #                        height=50)
            # self.return_buttons.add_widget(self.save_btn)
            # self.exit_btn = Button(text="Exit",
            #                        size_hint=(None, None),
            #                        bold=True,
            #                        #background_normal = 'buttons/Run.png',
            #                        #background_down = 'buttons/Run_Pressed.png',
            #                        #pos_hint= {"center_x": 0.5},
            #                        height=50)
            # self.return_buttons.add_widget(self.exit_btn)
            # self.layout.add_widget(self.return_buttons)


            
            # #self.layout.add_widget(self.settings_grid)


            # self.add_widget(self.layout)

            self.settings_layout = GridLayout(cols=2)
            #self.brightnessControl = Slider(min = 0, max = 100)

            self.complexity_prompt = Label(text="Model Complexity",
                                           color="#c3c3c3")

            self.settings_layout.add_widget(self.complexity_prompt)

            self.btn_group = BoxLayout(orientation='horizontal')
            self.btn_group.height = 50
            self.simple_btn = ToggleButton(text='Simple', group='complexity', state='down')
            self.complex_btn = ToggleButton(text='Complex', group='complexity', state='normal')
            self.btn_group.add_widget(self.simple_btn)
            self.btn_group.add_widget(self.complex_btn)
            self.settings_layout.add_widget(self.btn_group)




            self.det_conf_prompt = Label(text="Min Detection Confidence",
                                         color="#c3c3c3",
                                         )

            self.det_conf_slider = Slider(min=0.5, 
                                          max=1, 
                                          value=float(self.min_det_conf), 
                                          value_track=True, 
                                          value_track_color=[1, 0, 0, 1])
            self.det_conf_slider.bind(value=self.updateDetConfIndicator)

            self.det_conf_ind = Label(text=str(self.det_conf_slider.value),
                                      color="#c3c3c3")

            # 1st row - one label, one slider   
            self.settings_layout.add_widget(self.det_conf_prompt)

            self.slider_group_1 = BoxLayout(orientation='horizontal')
            self.slider_group_1.add_widget(self.det_conf_slider)
            self.slider_group_1.add_widget(self.det_conf_ind)
            self.settings_layout.add_widget(self.slider_group_1)


            self.track_conf_prompt = Label(text="Min Tracking Confidence",
                                         color="#c3c3c3",
                                         )

            self.track_conf_slider = Slider(min=0.5, 
                                            max=1, 
                                            value=float(self.min_track_conf), 
                                            value_track=True, 
                                            value_track_color=[1, 0, 0, 1])
            self.track_conf_slider.bind(value=self.updateTrackConfIndicator)

            self.track_conf_ind = Label(text=str(self.track_conf_slider.value),
                                      color="#c3c3c3")

            # 1st row - one label, one slider   
            self.settings_layout.add_widget(self.track_conf_prompt)

            self.slider_group_2 = BoxLayout(orientation='horizontal')
            self.slider_group_2.add_widget(self.track_conf_slider)
            self.slider_group_2.add_widget(self.track_conf_ind)
            self.settings_layout.add_widget(self.slider_group_2)


            
            self.confirmation_box = BoxLayout(orientation='horizontal', pos_hint={"center_x": 0.7})
            self.confirmation_box.pos_hint = {"center_x": 0.7}
            self.save_btn = Button(text="",
                                   size_hint=(None, None),
                                   bold=True,
                                   background_normal = 'buttons/ApplyChanges.png',
                                   background_down = 'buttons/ApplyChanges_Pressed.png',
                                   #pos_hint= {"center_x": 0.7},
                                   width=round(current_width/6.41),
                                   height=round(current_height/10.8))

            self.save_btn.bind(on_press=self.updateSavedVals)

            self.confirmation_box.add_widget(self.save_btn)
            self.exit_btn = Button(text="",
                                   size_hint=(None, None),
                                   bold=True,
                                   background_normal = 'buttons/Cancel.png',
                                   background_down = 'buttons/Cancel_Pressed.png',
                                   #pos_hint= {"center_x": 0.7},
                                   width=round(current_width/11.52),
                                   height=round(current_height/10.8))
            self.exit_btn.bind(on_press=self.goToMain)
            self.confirmation_box.add_widget(self.exit_btn)
            self.confirmation_box.pos_hint= {"center_x": 0.9}

            self.settings_layout.add_widget(Label(text=""))
            self.settings_layout.add_widget(self.confirmation_box)

            self.parent_component.add_widget(self.settings_layout)
            #self.parent_component.add_widget(self.confirmation_box)

            self.group_logo = Image(source="images/Logo_White_A_Cropped.png",
                                pos_hint={"center_x": 0.95, "bottom": 0},
                                size_hint=(None, None),
                                width=round(current_width/18.46),
                                height=round(current_height/9.75))
            #self.group_logo.size_hint = (None, 0.2)
            self.add_widget(self.group_logo)
    


        def updateDetConfIndicator(self, *args):
            self.det_conf_ind.text=str(round(self.det_conf_slider.value, 2))

        def updateTrackConfIndicator(self, *args):
            self.track_conf_ind.text=str(round(self.track_conf_slider.value, 2))

        def updateSavedVals(self, *args):
            self.min_track_conf = float(self.track_conf_ind.text)
            self.min_det_conf = float(self.det_conf_ind.text)
            if self.simple_btn.state == "down":
                self.model_complexity = 0
            else:
                self.model_complexity = 1

            self.model_store.modifyModelParams(self.model_complexity, self.min_det_conf, self.min_track_conf)

        def goToMain(self, *args):
            self.det_conf_slider.value = float(self.min_det_conf)
            self.track_conf_slider.value = float(self.min_track_conf)
            self.manager.current = 'main'
