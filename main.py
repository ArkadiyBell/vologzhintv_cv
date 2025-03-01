import numpy as np
import matplotlib.pyplot as plt


external = np.diag([1, 1, 1, 1]).reshape(4, 2, 2)

internal = np.logical_not(external)

cross = np.array([[[1, 0], [0, 1]], [[0, 1], [1, 0]]])


def match(a, masks):
    a = np.array([[1  if a[i][j] != 0 else 0 for j in range(2)] for i in range(2)])
    for mask in masks:
        if np.all(a == mask):
            return True
    return False


def count_objects(image):
    E = 0
    for y in range(0, image.shape[0] - 1):
        for x in range(0, image.shape[1] - 1):
            sub = image[y : y + 2, x : x + 2]
            if match(sub, external):
                E += 1
            elif match(sub, internal):
                E -= 1
            elif match(sub, cross):
                E += 2
    return E / 4

image = np.load("example2.npy")


plt.imshow(image)
count = 0
if (len(image.shape) < 3):
    image = image.reshape(image.shape[0],image.shape[1],1)
for s in range(image.shape[2]): 
    img = np.array([[image[i][j][s] for j in range(image.shape[1]) ] for i in range(image.shape[0])])
    count += count_objects(img)
plt.show()
print(count)