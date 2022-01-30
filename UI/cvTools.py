import cv2


def initializeWebcam():
    vid = cv2.VideoCapture(0)
    return vid

def captureFrame(vid):
    ret, frame = vid.read()

    return frame

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