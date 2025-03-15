import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label
from skimage.morphology import (binary_closing, binary_dilation, binary_erosion, binary_opening)

masks = np.array([[[1, 0, 1],
                   [0, 1, 0],
                   [1, 0, 1]],

                  [[0, 1, 0],
                   [1, 1, 1],
                   [0, 1, 0]]])

def match(a, masks):
    for mask in masks:
        if np.all(a == mask):
            return True
    return False

space = np.load("stars.npy")
sum = 0
for i in range(space.shape[0]-2):
    for j in range(space.shape[1]-2):
        sub = space[i:i+3, j:j+3]
        
        if match(sub, masks):
            sum +=1
print("Решение 1 способом(без использования морфологии): " + str(sum))

notStar = np.array([[1,1,1],
                 [1,1,1]])



notStars = binary_opening(space, notStar)
labeled_notStars=label(notStars)

print(f"Решение 2 способом: {np.max(label(space)) - np.max(labeled_notStars)}")
