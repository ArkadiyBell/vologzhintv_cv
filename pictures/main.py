import cv2
import numpy as np



vid = cv2.VideoCapture("output.avi")
count = 0

while True:
    ret, frame = vid.read()
    if not ret:
        break
    avg_color = np.average(np.average(np.average(frame, axis=0), axis=0))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) == 7 and avg_color < 30:
        count += 1

print(count)
vid.release()
