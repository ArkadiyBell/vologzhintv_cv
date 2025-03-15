import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label
from skimage.morphology import (binary_closing, binary_dilation, binary_erosion, binary_opening)

files = [f".\imgs\wires{_}npy.txt" for _ in range(1, 7)]

for file in files:
    print("Изображение: " + file)
    data = np.load(file)

    labeled = label(data)

    for _ in range(1, np.max(labeled) + 1):

        result = binary_erosion(labeled==_, np.ones(3).reshape(3, 1))

        destroyed = np.max(label(result))
        if destroyed > 1:
            print(f"Провод {_} разделен на {destroyed} част.")
        elif destroyed == 1:
            print (f"Провод {_} цел")
        else:
            print(f"Провод {_} Уничтожен")

        plt.subplot(121)
        plt.imshow(labeled)
        plt.subplot(122)
        plt.imshow(result)
        plt.show()
