import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

index_status = "NA"

# For static images:
# IMAGE_FILES = []
# with mp_hands.Hands(
#     static_image_mode=True,
#     max_num_hands=2,
#     min_detection_confidence=0.5) as hands:
#   for idx, file in enumerate(IMAGE_FILES):
#     # Read an image, flip it around y-axis for correct handedness output (see
#     # above).
#     image = cv2.flip(cv2.imread(file), 1)
#     # Convert the BGR image to RGB before processing.
#     results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

#     # Print handedness and draw hand landmarks on the image.
#     print('Handedness:', results.multi_handedness)
#     if not results.multi_hand_landmarks:
#       continue
#     image_height, image_width, _ = image.shape
#     annotated_image = image.copy()
#     for hand_landmarks in results.multi_hand_landmarks:
#       print('hand_landmarks:', hand_landmarks)
#       print(
#           f'Index finger tip coordinates: (',
#           f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width}, '
#           f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height})'
#       )
#       mp_drawing.draw_landmarks(
#           annotated_image,
#           hand_landmarks,
#           mp_hands.HAND_CONNECTIONS,
#           mp_drawing_styles.get_default_hand_landmarks_style(),
#           mp_drawing_styles.get_default_hand_connections_style())
#     cv2.imwrite(
#         '/tmp/annotated_image' + str(idx) + '.png', cv2.flip(annotated_image, 1))
#     # Draw hand world landmarks.
#     if not results.multi_hand_world_landmarks:
#       continue
#     for hand_world_landmarks in results.multi_hand_world_landmarks:
#       mp_drawing.plot_landmarks(
#         hand_world_landmarks, mp_hands.HAND_CONNECTIONS, azimuth=5)

# For webcam input:
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)



    hand_landmarks = results.multi_hand_landmarks #produces xyz coordinates for all landmark points
    #data is in a list with one index (for one hand), containing element of type 'mediapipe.framework.formats.landmark_pb2.NormalizedLandmarkList'

    #For y coordinates, top of screen is -1, bottom of screen is 1
    if hand_landmarks:
        tip = hand_landmarks[0].landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
        below_tip = hand_landmarks[0].landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].y
        before_end = hand_landmarks[0].landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y
        end = hand_landmarks[0].landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y
        if tip < below_tip:
            index_status = "1"
            #print("0")
        elif tip < before_end and tip > below_tip:
            index_status = "0.66"
            #print("0.33")
        elif tip > below_tip and tip < end:
            index_status = "0.33"
            #print("0.66")
        elif tip > end:
            index_status = "0"
            #print("1")
        #print(tip, end)

# #           f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
#     if points:
#         print(type(points[0][0]))
#     #print(results.multi_hand_landmarks)

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





    font = cv2.FONT_HERSHEY_SIMPLEX
    org = (25, 25)
    fontScale = 0.5
    color = (255, 0, 0)
    thickness = 2
    image = cv2.putText(image, 'Status: ' + index_status, org, font, fontScale, color, thickness, cv2.LINE_AA)






    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()