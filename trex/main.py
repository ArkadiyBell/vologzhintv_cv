from mss import mss
import pyautogui
import cv2
import numpy as np
import time

save_folder = "saved_images"
window_width, window_height = 640, 100
crop_area = {'top': 335, 'left': 204, 'width': 720, 'height': 59}
min_contour_area = 100

roi_params = {'min_x': 0, 'max_x': 640, 'min_y': 0, 'max_y': 100}
prev_time = time.perf_counter()
prev_cacti = np.array([])
time_jumps = [0,0]
time_downs = []
speeds = []
prev_time_jumps=[0,0]
prev_speed = 400
speed = 400
differ= 0
pyautogui.keyDown('down')
with mss() as sct:
    while True:

        screenshot = sct.grab(crop_area)
        curr_time = time.perf_counter()
        img = np.array(screenshot)[..., :3]

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        binary_inv = 255 - binary 
        contours, _ = cv2.findContours(binary_inv, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        stage1 = np.full_like(binary, 255)
        for cnt in contours:
            if cv2.contourArea(cnt) > 5 and cv2.contourArea(cnt) < 700:
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(stage1, (x, y), (x+w, y+h), 0, -1)
        dilated = cv2.dilate(255 - stage1, np.ones((7,7)), iterations=2)
        contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        final = np.full_like(binary, 255)
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(final, (x, y), (x+w, y+h), 0, -1)


        barriers = np.array(final)[-1, :]
        diffs = np.diff(barriers)
        starts = np.where(diffs == 1)[0] + 1  
        ends = np.where(diffs == 255)[0] + 1  
        if barriers[0] == 0:
            starts = np.insert(starts, 0, 0)
        if barriers[-1] == 0:
            ends = np.append(ends, len(barriers))

        cacti = []
        for  end, start in zip(ends, starts):
            length = end - start
            cacti.append([start, length])
        cacti = np.array(cacti)
        length_tolerance = 5
        matches = []

        for curr in cacti:
            for prev in prev_cacti:
                if abs(curr[1] - prev[1]) <= length_tolerance and prev[0] > curr[0]:
                    matches.append([curr.tolist(), prev.tolist()])
        time_jumps = [0,0]
        if matches:

            matches.sort(key=lambda x: x[0][0])
            match = matches[0]
            speed = (match[1][0] - match[0][0])/(curr_time-prev_time)
            if speed > prev_speed*1.8:
                speed=prev_speed
            speeds.append(speed)
            speed = sum(speeds)/len(speeds)
            wait_jump = (match[0][0]/speed - 0.3)
            wait_land = (match[0][0] + match[0][1])/speed - 0.19

            if  0 < wait_jump < 0.03:
                jump_time = curr_time + wait_jump
                land_time = curr_time + wait_land
                time_jumps[0]=jump_time
                time_jumps[1]=land_time
            elif wait_jump <0:
                jump_time = curr_time
                land_time = curr_time + wait_land
                time_jumps[0]=jump_time
                time_jumps[1]=land_time
        else:
            pyautogui.keyDown('down')

        
        if time_jumps[0]:
            print(wait_jump)
            print(len(speeds))
            pyautogui.keyUp("down")
            #print(speed)
            time.sleep(abs(time_jumps[0] - curr_time))
            pyautogui.press('up')
            #print('вверх')
            cv2.imshow("Screen", img)
             
            time.sleep(abs(time_jumps[1]-time_jumps[0]))
            
            prev_speed = speed
            speeds = []
            pyautogui.keyDown('down')

        resized = cv2.resize(final, (window_width, window_height))


        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        prev_time = curr_time
        prev_cacti = cacti
        prev_time_jumps = time_jumps

cv2.destroyAllWindows()
