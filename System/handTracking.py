import cv2
import mediapipe as mp
import numpy as np
#import pythonSerial
import time
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
from google.protobuf.json_format import MessageToDict
from mediapipe.framework.formats import landmark_pb2
hand_indicator = cv2.imread("images/hand_placement_indicator_small.png")

def initializeWebcam():
    vid = cv2.VideoCapture(0)
    return vid

def captureFrame(vid):
    ret, frame = vid.read()

    return frame



class HandTracker:
    def __init__(self, model_complexity=1, min_detection_conf=0.5, min_track_conf=0.5):
        #Set model parameter settings
        self.model_complexity = model_complexity
        self.min_detection_conf = min_detection_conf
        self.min_track_conf = min_track_conf

        self.thumb_tip = 0
        self.thumb_below_tip = 0 
        self.thumb_before_end = 0 
        self.thumb_end = 0

        self.index_tip = 0
        self.index_below_tip = 0 
        self.index_before_end = 0 
        self.index_end = 0

        self.mid_tip = 0
        self.mid_below_tip = 0 
        self.mid_before_end = 0 
        self.mid_end = 0

        self.ring_tip = 0
        self.ring_below_tip = 0 
        self.ring_before_end = 0 
        self.ring_end = 0

        self.pinky_tip = 0
        self.pinky_below_tip = 0 
        self.pinky_before_end = 0 
        self.pinky_end = 0

        self.index_status = "NA"
        self.mid_status = "NA"
        self.ring_status = "NA"
        self.pinky_status = "NA"
        self.thumb_status = "NA"
        self.output = [0,0,0,0,0]

        self.none_count = 0 #Poll for number of none's detected


    def addHandOverlay(self, frame):
        old_image_height, old_image_width = hand_indicator.shape[0], hand_indicator.shape[1]
        channels = 3

        # create new image of desired size and color (blue) for padding
        new_image_width = 1280
        new_image_height = 720
        color = (255,255,255)
        result = np.full((new_image_height,new_image_width, channels), color, dtype=np.uint8)

        # compute center offset
        x_center = (new_image_width - old_image_width) // 2
        y_center = (new_image_height - old_image_height) // 2

        # copy img image into center of result image
        result[y_center:y_center+old_image_height, 
            x_center:x_center+old_image_width] = hand_indicator

        return cv2.addWeighted(frame, 0.4, result, 0.1, 0)


    def calibrationStep(self, frame, count):
        font = cv2.FONT_HERSHEY_DUPLEX
        text = str(count)

        #org = (50, 50)
        fontScale = 10
        color = (255, 255, 255)
        thickness = 2

        textSize = cv2.getTextSize(text=str(count), fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=10, thickness=2)[0]
        text_height = textSize[1]
        text_width = textSize[0]

        textX = int((frame.shape[1] - text_width) / 2)
        textY = int((frame.shape[0] + text_height) / 2)


        frame = cv2.putText(frame, text, (textX, textY), font, fontScale, color, thickness, cv2.LINE_AA)

        return frame

    #Returns presence of hand on screen and handedness (left, right)
    def checkHandTrack(self, frame):
        with mp_hands.Hands(model_complexity=0, min_detection_confidence=0.5) as hands:
            results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

            if results.multi_handedness:
                for idx, hand_handedness in enumerate(results.multi_handedness):
                    handedness_dict = MessageToDict(hand_handedness)
                    handedness = handedness_dict["classification"][0]["label"]
            else:
                handedness = "None"

            return handedness

            # if handedness == "Right":
            #     return "Right"
            # elif handedness == "Left":
            #     return "Left"
            # else:
            #     return handedness

    def postProcess(self, hand_landmarks, major_hand_idx):
        # For y coordinates, top of screen is -1, bottom of screen is 1
        if hand_landmarks:
            # for the thumb
            self.thumb_tip = hand_landmarks[major_hand_idx].landmark[mp_hands.HandLandmark.THUMB_TIP].x
            self.thumb_below_tip = hand_landmarks[major_hand_idx].landmark[mp_hands.HandLandmark.THUMB_IP].x
            self.thumb_before_end = hand_landmarks[major_hand_idx].landmark[mp_hands.HandLandmark.THUMB_MCP].x
            self.thumb_end = hand_landmarks[major_hand_idx].landmark[mp_hands.HandLandmark.THUMB_CMC].x
            if self.thumb_tip < self.thumb_below_tip:
                self.thumb_status = "1"
                self.output[0] = 0
            elif self.thumb_tip < (self.thumb_before_end) and self.thumb_tip >= (self.thumb_below_tip):
                self.thumb_status = "0.66"
                self.output[0] = 60
            elif self.thumb_tip > (self.thumb_before_end + 0.01) and self.thumb_tip < (self.thumb_end - 0.01):
                self.thumb_status = "0.33"
                self.output[0] = 120
            elif self.thumb_tip > self.thumb_end:
                self.thumb_status = "0"
                self.output[0] = 150

            # for the index finger
            self.index_tip = hand_landmarks[major_hand_idx].landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
            self.index_below_tip = hand_landmarks[major_hand_idx].landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].y
            self.index_before_end = hand_landmarks[major_hand_idx].landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y
            self.index_end = hand_landmarks[major_hand_idx].landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y
            if self.index_tip < self.index_below_tip:
                self.index_status = "1"
                self.output[1] = 0
            elif self.index_tip < (self.index_before_end) and self.index_tip >= (self.index_below_tip):
                self.index_status = "0.66"
                self.output[1] = 60
            elif self.index_tip > (self.index_before_end + 0.01) and self.index_tip < (self.index_end - 0.01):
                self.index_status = "0.33"
                self.output[1] = 120
            elif self.index_tip > self.index_end:
                self.index_status = "0"
                self.output[1] = 180

            # for the middle finger
            self.mid_tip = hand_landmarks[major_hand_idx].landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y
            self.mid_below_tip = hand_landmarks[major_hand_idx].landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP].y
            self.mid_before_end = hand_landmarks[major_hand_idx].landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y
            self.mid_end = hand_landmarks[major_hand_idx].landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y
            if self.mid_tip < self.mid_below_tip:
                self.mid_status = "1"
                self.output[2] = 0
            elif self.mid_tip < (self.mid_before_end) and self.mid_tip >= (self.mid_below_tip):
                self.mid_status = "0.66"
                self.output[2] = 60
            elif self.mid_tip > (self.mid_before_end + 0.01) and self.mid_tip < (self.mid_end - 0.01):
                self.mid_status = "0.33"
                self.output[2] = 120
            elif self.mid_tip > self.mid_end:
                self.mid_status = "0"
                self.output[2] = 180

            # for the ring finger
            self.ring_tip = hand_landmarks[major_hand_idx].landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y
            self.ring_below_tip = hand_landmarks[major_hand_idx].landmark[mp_hands.HandLandmark.RING_FINGER_DIP].y
            self.ring_before_end = hand_landmarks[major_hand_idx].landmark[mp_hands.HandLandmark.RING_FINGER_PIP].y
            self.ring_end = hand_landmarks[major_hand_idx].landmark[mp_hands.HandLandmark.RING_FINGER_MCP].y
            if self.ring_tip < self.ring_below_tip:
                self.ring_status = "1"
                self.output[3] = 0
            elif self.ring_tip < (self.ring_before_end) and self.ring_tip >= (self.ring_below_tip):
                self.ring_status = "0.66"
                self.output[3] = 60
            elif self.ring_tip > (self.ring_before_end + 0.01) and self.ring_tip < (self.ring_end - 0.01):
                self.ring_status = "0.33"
                self.output[3] = 120
            elif self.ring_tip > self.ring_end:
                self.ring_status = "0"
                self.output[3] = 180

            # for the pinky finger
            self.pinky_tip = hand_landmarks[major_hand_idx].landmark[mp_hands.HandLandmark.PINKY_TIP].y
            self.pinky_below_tip = hand_landmarks[major_hand_idx].landmark[mp_hands.HandLandmark.PINKY_DIP].y
            self.pinky_before_end = hand_landmarks[major_hand_idx].landmark[mp_hands.HandLandmark.PINKY_PIP].y
            self.pinky_end = hand_landmarks[major_hand_idx].landmark[mp_hands.HandLandmark.PINKY_MCP].y
            if self.pinky_tip < self.pinky_below_tip:
                self.pinky_status = "1"
                self.output[4] = 0
            elif self.pinky_tip < (self.pinky_before_end) and self.pinky_tip >= (self.pinky_below_tip):
                self.pinky_status = "0.66"
                self.output[4] = 60
            elif self.pinky_tip > (self.pinky_before_end + 0.01) and self.pinky_tip < (self.pinky_end - 0.01):
                self.pinky_status = "0.33"
                self.output[4] = 120
            elif self.pinky_tip > self.pinky_end:
                self.pinky_status = "0"
                self.output[4] = 180

            #isWorking = pythonSerial.transmit(self.output)
            #time.sleep(1)


    def putFingerVals(self, frame):
        font = cv2.FONT_HERSHEY_SIMPLEX
        org = (25, 25)
        fontScale = 0.5
        color = (255, 0, 0)
        thickness = 2
        frame = cv2.putText(frame, 'Thumb Status: ' + self.thumb_status, (20, 30), font, fontScale, color, thickness, cv2.LINE_AA)
        frame = cv2.putText(frame, 'Index Status: ' + self.index_status, (20, 50), font, fontScale, color, thickness, cv2.LINE_AA)
        frame = cv2.putText(frame, 'Middle Status: ' + self.mid_status, (20, 70), font, fontScale, color, thickness, cv2.LINE_AA)
        frame = cv2.putText(frame, 'Ring Status: ' + self.ring_status, (20, 90), font, fontScale, color, thickness, cv2.LINE_AA)
        frame = cv2.putText(frame, 'Pinky Status: ' + self.pinky_status, (20, 110), font, fontScale, color, thickness, cv2.LINE_AA)

        return frame


    def performHandTracking(self, frame):
        with mp_hands.Hands(model_complexity=self.model_complexity, 
                            min_detection_confidence=self.min_detection_conf, 
                            min_tracking_confidence=self.min_track_conf) as hands:
            results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

            hand_landmarks = results.multi_hand_landmarks #produces xyz coordinates for all landmark points
            #data is in a list with one index (for one hand), containing element of type
            # 'mediapipe.framework.formats.landmark_pb2.NormalizedLandmarkList'
            # print(results.multi_hand_landmarks)
            # print("Next:")

            right_hand_list = []
            if results.multi_handedness:
                for idx, hand_handedness in enumerate(results.multi_handedness): 
                    #results.multi_handedness is of type <class 'mediapipe.framework.formats.classification_pb2.ClassificationList'>
                    handedness_dict = MessageToDict(hand_handedness)
                    handedness = handedness_dict["classification"][0]["label"]
                    if handedness == "Right":
                        right_hand_list.append(idx)

            if right_hand_list:
                self.postProcess(hand_landmarks,right_hand_list[0])
                hand_landmark_major_right = landmark_pb2.NormalizedLandmarkList(
                    landmark = [
                        hand_landmarks[right_hand_list[0]].landmark[i] for i in range(21) 
                    ]
                )
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(
                            frame,
                            hand_landmark_major_right,
                            mp_hands.HAND_CONNECTIONS,
                            mp_drawing_styles.get_default_hand_landmarks_style(),
                            mp_drawing_styles.get_default_hand_connections_style())

                frame = self.putFingerVals(frame)
            else:
                self.postProcess(hand_landmarks,0)

            if not results.multi_hand_landmarks:
                self.none_count += 1
                if self.none_count >= 10:
                    hand_detected = False
                else:
                    hand_detected = True
            else:
                hand_detected = True
                self.none_count = 0

            return frame, hand_detected




    # Read an image, flip it around y-axis for correct handedness output (see
    # above).

    #count_img = cv2.imread(str(count)+'.png')

    # x_offset=y_offset=50
    # frame[y_offset:y_offset+count_img.shape[0], x_offset:x_offset+count_img.shape[1]] = count_img

    # h, w = count_img.shape[0], count_img.shape[1]
    # count_img = cv2.flip(count_img, 1)
    # hh, ww = frame.shape[0], frame.shape[1]

    # # compute xoff and yoff for placement of upper left corner of resized image   
    # yoff = round((hh-h)/2)
    # xoff = round((ww-w)/2)

    # # use numpy indexing to place the resized image in the center of background image
    # result = frame.copy()
    # result[yoff:yoff+h, xoff:xoff+w] = count_img

    #return result