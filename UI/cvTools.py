import cv2


def initializeWebcam():
    vid = cv2.VideoCapture(0)
    return vid

def captureFrame(vid):
    ret, frame = vid.read()

    return frame