#important libraries
import pickle
import cv2
import mediapipe as mp
import numpy as np
import pyautogui
from pyautogui import click, displayMousePosition, typewrite, hotkey
import time
#Load the trained model from a pickle file:
model_dict = pickle.load(open('./model.p', 'rb'))
model = model_dict['model']

#Initialize the webcam:
cap = cv2.VideoCapture(0)

#Initialize the MediaPipe Hands module:
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

#Define a dictionary mapping class indices to labels:
labels_dict = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4:'E', 5:'F', 6:'G',7:'H', 8:'I'}

#Main loop for real-time gesture recognition:
while True:
##
    #Initialization:
    data_aux = []
    x_ = []
    y_ = []

    ret, frame = cap.read()

    H, W, _ = frame.shape

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    #Hand Landmark Detection and Normalization:
    results = hands.process(frame_rgb)

    #checks if there are multiple hand landmarks detected in the frame.
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks: #draws the detected hand landmarks on the frame for visualization.
            mp_drawing.draw_landmarks(
                frame,  # image to draw
                hand_landmarks,  # model output
                mp_hands.HAND_CONNECTIONS,  # hand connections
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())

        for hand_landmarks in results.multi_hand_landmarks: 
            #iterate over each detected hand landmark, extract its x and y coordinates, and store them in `x_` and `y_` lists.
            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y

                x_.append(x)
                y_.append(y)

            #normalizes the coordinates by subtracting the minimum x and y coordinates from all coordinates in `x_` and `y_`, respectively, and appends them to `data_aux`.
            for i in range(len(hand_landmarks.landmark)): 
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                data_aux.append(x - min(x_))
                data_aux.append(y - min(y_))

        x1 = int(min(x_) * W) - 10
        y1 = int(min(y_) * H) - 10

        x2 = int(max(x_) * W) - 10
        y2 = int(max(y_) * H) - 10

        #Gesture Prediction and Display:
        prediction = model.predict([np.asarray(data_aux)])
        predicted_character = labels_dict[int(prediction[0])]
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
        if predicted_character=='D':
            pyautogui.press('volumeup')
        elif predicted_character=='E':
            pyautogui.press('volumedown')
        elif predicted_character=='F':
            click(189, 56)
            typewrite('youtube.com')
            hotkey('enter')
            time.sleep(4)
        elif predicted_character == 'G':
            pyautogui.press('volumemute')
            time.sleep(4)

        else:       
            cv2.putText(frame, predicted_character, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3,
                        cv2.LINE_AA)
       
    #Display the Frame:
    cv2.imshow('frame', frame)
    cv2.waitKey(1)

#Release the webcam and close all windows: 
cap.release()
cv2.destroyAllWindows()
