import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import regionprops,label
from skimage.filters import sobel, threshold_otsu
from scipy.ndimage import binary_fill_holes

def isPensil(region, size):
    cy,cx = region.centroid_local
    cx/=region.image.shape[1]
    cy/=region.image.shape[0]
    not_rounded = region.area/region.perimeter**2 <0.03
    length = (region.image.shape[0]**2+region.image.shape[1]**2)**0.5
    if 0.25*region.perimeter/length < 1.38 and not_rounded and length>size/2 and length < size and \
        0.25*region.perimeter/length > 0.62 and abs(cx - 0.5) < 0.1 and abs(cy - 0.5) < 0.1:
        return True
    return False
count_all = 0
for i in range(1,13):
    image = plt.imread(f"./images/img ({i}).jpg").mean(axis = 2)
    s = sobel(image)

    thresh = threshold_otsu(s)/2
    s[s < thresh] = 0
    s[s >= thresh] = 1
    s = binary_fill_holes(s, np.ones((3,3)))
    labeled = (label(s))
    regions = regionprops(labeled)
    regions = sorted(regions, key = lambda item: item.perimeter)
    count = 0
    size=np.min(labeled.shape)
    for region in regions[-10:]:
        count += isPensil(region, size)
    print(f'На {i} изображении {count} карандашей')
    count_all+= count
print(f'На всех изображениях {count_all} карандашей')