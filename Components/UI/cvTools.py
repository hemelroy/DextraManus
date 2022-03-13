import cv2
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
from google.protobuf.json_format import MessageToDict

hand_indicator = cv2.imread("hand_placement_indicator_small.png")

def initializeWebcam():
    vid = cv2.VideoCapture(0)
    return vid

def captureFrame(vid):
    ret, frame = vid.read()

    return frame

def addHandOverlay(frame):
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

def calibrationStep(frame, count):
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

def checkHandTrack(frame):
    with mp_hands.Hands(model_complexity=0, min_detection_confidence=0.5) as hands:
        results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        if results.multi_handedness:
            for idx, hand_handedness in enumerate(results.multi_handedness):
                handedness_dict = MessageToDict(hand_handedness)
                handedness = handedness_dict["classification"][0]["label"]
        else:
            handedness = "None"

        
        if handedness == "Right":
            return True
        else:
            return False



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