import cv2
import numpy as np

cv2.namedWindow("Camera", cv2.WINDOW_NORMAL)
glasses = cv2.imread('deal-with-it.png')
print(np.unique(glasses))
gray_glasses = cv2.cvtColor(glasses, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray_glasses, 10, 255, cv2.THRESH_BINARY)
mask_glasses = np.zeros_like(glasses)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
for i, contour in enumerate(contours):
    if i == 1:
        cv2.drawContours(mask_glasses, [contour], -1, (255, 255, 255), cv2.FILLED)

print(glasses.shape)
capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)

def censore(image, size = (5, 5)):
    result = np.zeros_like(image)
    stepy = result.shape[0]//size[0]
    stepx = result.shape[1]//size[1]
    for y in range(0, image.shape[0], stepy):
        for x in range(0, image.shape[1], stepx):
            for c in range(0, image.shape[2]):
             result[y:y+stepy, x:x+stepx, c] = np.mean(image[y:y+stepy, x:x+stepx, c])


    return result

face_cascade = cv2.CascadeClassifier("haarcascade-frontalface-default.xml")
eye_cascade = cv2.CascadeClassifier("haarcascade-eye.xml")

while capture.isOpened():
    
    ret, frame = capture.read()
    blurred = cv2.GaussianBlur(frame, (11,11), 0)
    gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
    eyes = eye_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=20)
    centroids = []
    points = []
    for x, y, w, h in eyes[:2]:
        centroids.append([x+w/2, y+h/2])
        points.append(x)
        points.append(x+w)

    if len(centroids) ==2 :
        x_center = int((centroids[0][0] + centroids[1][0]) // 2)
        y_center = int((centroids[0][1] + centroids[1][1]) // 2)
        width = max(points) - min(points)
        
        k = 1.5*width / glasses.shape[1]
        new_size = (int(glasses.shape[1] * k), int(glasses.shape[0] * k))
        
        glasses_new = cv2.resize(glasses, new_size)
        mask_new = cv2.resize(mask_glasses, new_size)
        
        y_start = y_center - glasses_new.shape[0] // 2
        y_end = y_start + glasses_new.shape[0]
        x_start = x_center - glasses_new.shape[1] // 2
        x_end = x_start + glasses_new.shape[1]

        roi = frame[y_start:y_end, x_start:x_end]
        
        mask_gray = cv2.cvtColor(mask_new, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(mask_gray, 1, 255, cv2.THRESH_BINARY)
        
        masked_glasses = cv2.bitwise_and(glasses_new, glasses_new, mask=mask)
        masked_bg = cv2.bitwise_and(roi, roi, mask=cv2.bitwise_not(mask))
        combined = cv2.add(masked_bg, masked_glasses)
        
        frame[y_start:y_end, x_start:x_end] = combined

    key = chr(cv2.waitKey(1) & 0xFF)
    if key == "q":
        break
    cv2.imshow("Camera", frame)
capture.release()
cv2.destroyAllWindows()