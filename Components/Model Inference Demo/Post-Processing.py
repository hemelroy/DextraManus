import numpy as np
import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

index_status = "NA"
mid_status = "NA"
ring_status = "NA"
pinky_status = "NA"
thumb_status = "NA"
output = [0,0,0,0,0]

# For webcam input
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)


    hand_landmarks = results.multi_hand_landmarks #produces xyz coordinates for all landmark points
    #data is in a list with one index (for one hand), containing element of type
    # 'mediapipe.framework.formats.landmark_pb2.NormalizedLandmarkList'

    # For y coordinates, top of screen is -1, bottom of screen is 1
    if hand_landmarks:

        # for the thumb
        thumb_tip = hand_landmarks[0].landmark[mp_hands.HandLandmark.THUMB_TIP].y
        thumb_below_tip = hand_landmarks[0].landmark[mp_hands.HandLandmark.THUMB_IP].y
        thumb_before_end = hand_landmarks[0].landmark[mp_hands.HandLandmark.THUMB_MCP].y
        thumb_end = hand_landmarks[0].landmark[mp_hands.HandLandmark.THUMB_CMC].y
        if thumb_tip < thumb_below_tip:
            thumb_status = "1"
            output[0] = 0
        elif thumb_tip < (thumb_before_end) and thumb_tip >= (thumb_below_tip):
            thumb_status = "0.66"
            output[0] = 60
        elif thumb_tip > (thumb_before_end + 0.01) and thumb_tip < (thumb_end - 0.01):
            thumb_status = "0.33"
            output[0] = 120
        elif thumb_tip > thumb_end:
            thumb_status = "0"
            output[0] = 150

        # for the index finger
        index_tip = hand_landmarks[0].landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
        index_below_tip = hand_landmarks[0].landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].y
        index_before_end = hand_landmarks[0].landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y
        index_end = hand_landmarks[0].landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y
        if index_tip < index_below_tip:
            index_status = "1"
            output[1] = 0
        elif index_tip < (index_before_end) and index_tip >= (index_below_tip):
            index_status = "0.66"
            output[1] = 60
        elif index_tip > (index_before_end + 0.01) and index_tip < (index_end - 0.01):
            index_status = "0.33"
            output[1] = 120
        elif index_tip > index_end:
            index_status = "0"
            output[1] = 180

        # for the middle finger
        mid_tip = hand_landmarks[0].landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y
        mid_below_tip = hand_landmarks[0].landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP].y
        mid_before_end = hand_landmarks[0].landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y
        mid_end = hand_landmarks[0].landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y
        if mid_tip < mid_below_tip:
            mid_status = "1"
            output[2] = 0
        elif mid_tip < (mid_before_end) and mid_tip >= (mid_below_tip):
            mid_status = "0.66"
            output[2] = 60
        elif mid_tip > (mid_before_end + 0.01) and mid_tip < (mid_end - 0.01):
            mid_status = "0.33"
            output[2] = 120
        elif mid_tip > mid_end:
            mid_status = "0"
            output[2] = 180

        # for the ring finger
        ring_tip = hand_landmarks[0].landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y
        ring_below_tip = hand_landmarks[0].landmark[mp_hands.HandLandmark.RING_FINGER_DIP].y
        ring_before_end = hand_landmarks[0].landmark[mp_hands.HandLandmark.RING_FINGER_PIP].y
        ring_end = hand_landmarks[0].landmark[mp_hands.HandLandmark.RING_FINGER_MCP].y
        if ring_tip < ring_below_tip:
            ring_status = "1"
            output[3] = 0
        elif ring_tip < (ring_before_end) and ring_tip >= (ring_below_tip):
            ring_status = "0.66"
            output[3] = 60
        elif ring_tip > (ring_before_end + 0.01) and ring_tip < (ring_end - 0.01):
            ring_status = "0.33"
            output[3] = 120
        elif ring_tip > ring_end:
            ring_status = "0"
            output[3] = 180

        # for the pinky finger
        pinky_tip = hand_landmarks[0].landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y
        pinky_below_tip = hand_landmarks[0].landmark[mp_hands.HandLandmark.RING_FINGER_DIP].y
        pinky_before_end = hand_landmarks[0].landmark[mp_hands.HandLandmark.RING_FINGER_PIP].y
        pinky_end = hand_landmarks[0].landmark[mp_hands.HandLandmark.RING_FINGER_MCP].y
        if pinky_tip < pinky_below_tip:
            pinky_status = "1"
            output[4] = 0
        elif pinky_tip < (pinky_before_end) and pinky_tip >= (pinky_below_tip):
            pinky_status = "0.66"
            output[4] = 60
        elif pinky_tip > (pinky_before_end + 0.01) and pinky_tip < (pinky_end - 0.01):
            pinky_status = "0.33"
            output[4] = 120
        elif pinky_tip > pinky_end:
            pinky_status = "0"
            output[4] = 180

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())
    # Flip the image horizontally for a selfie-view display.
    image = cv2.flip(image, 1)

    # Placing the positions of each finger on the image
    font = cv2.FONT_HERSHEY_SIMPLEX
    org = (25, 25)
    fontScale = 0.5
    color = (255, 0, 0)
    thickness = 2
    image = cv2.putText(image, 'Thumb Status: ' + thumb_status, (20, 30), font, fontScale, color, thickness, cv2.LINE_AA)
    image = cv2.putText(image, 'Index Status: ' + index_status, (20, 50), font, fontScale, color, thickness, cv2.LINE_AA)
    image = cv2.putText(image, 'Middle Status: ' + mid_status, (20, 70), font, fontScale, color, thickness, cv2.LINE_AA)
    image = cv2.putText(image, 'Ring Status: ' + ring_status, (20, 90), font, fontScale, color, thickness, cv2.LINE_AA)
    image = cv2.putText(image, 'Pinky Status: ' + pinky_status, (20, 110), font, fontScale, color, thickness, cv2.LINE_AA)

    # Testing if the program generates the correct degrees of curl
    print(output)

    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()
