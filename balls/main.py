import cv2
import time
import numpy as np
import time
import json
import os
import random

def get_ball(image, color):
    lower = (np.max(color[0]) - 5, color[1] * 0.8, color[2] * 0.8)
    upper = (color[0] + 5, 255, 255)
    mask = cv2.inRange(image, lower, upper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL,
                                                cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        contour = max(contours, key=cv2.contourArea)
        (x, y), radius = cv2.minEnclosingCircle(contour)
        return True, (int(x), int(y), int(radius), mask)
    return False, (-1, -1, -1, np.array([-1]))

def get_color(image):
    x,y,w,h = cv2.selectROI("Color selection", image)
    x,y,w,h = int(x), int(y), int(w), int(h)
    roi = image[y:y+h, x:x+w]
    color = (np.median(roi[:,:,0]), np.median(roi[:,:,1]), np.median(roi[:,:,2]))
    cv2.destroyWindow("Color selection")
    return color

path = "settings.json"
if os.path.exists(path):
    base_colors = json.load(open(path, "r"))
else:
    base_colors = {}
game_started = False
guess_colors = []
roi = None
capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)



color = (7,150,250) #HSW Цвет шарика, узнали с помощью прошлой программы
lower = np.array([5,140, 175])
upper = np.array([9,255, 255])
cv2.namedWindow("Mask", cv2.WINDOW_NORMAL)
cv2.namedWindow("Camera", cv2.WINDOW_NORMAL)
prev_time = time.time()
points = []
game_colors = []
while capture.isOpened():
    ret, frame = capture.read()
    curr_time = time.time()
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    key = chr(cv2.waitKey(1) & 0xFF)


    if key == 'q':
        break
    if key in '1234':
        color = get_color(hsv)
        base_colors[key] = color
    balls = {}
    for key in base_colors:
        retr, (x, y, radius, mask) = get_ball(hsv, base_colors[key])
        if retr:
            cv2.imshow("Mask", mask)
            cv2.circle(frame, (x,y), radius, (255, 0, 255), 2)
            balls[key] = [x, y]
            result = []
            # balls = sorted(balls, key = lambda x : x[1])
            sorted_x = [key for key, value in sorted(balls.items(), key=lambda item: item[1][0])]
            sorted_y = [key for key, value in sorted(balls.items(), key=lambda item: item[1][1])]
            left = sorted_x[:2]
            top = sorted_y[:2]
            print(left)
            result.append((set(left) & set(top)))
            if left == top:
                print(result)
            # if len(sorted_keys) == 4:
            #     print(sorted_keys)
            # if sorted_keys == guess_colors:
            #     print("Победа!")




    if len(base_colors) == 4:
        if not game_started:
            guess_colors = list(base_colors)
            random.shuffle(guess_colors)
            game_started = True
            print(guess_colors)
    cv2.putText(frame, f"Game_started = {game_started}", (10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0))
    cv2.imshow("Camera", frame)
capture.release()
cv2.destroyAllWindows()
json.dump(base_colors, open(path, "w"))