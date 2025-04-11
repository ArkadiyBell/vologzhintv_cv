import matplotlib.pyplot as plt
import numpy as np
from skimage.measure import regionprops, label
from pathlib import Path

def count_vlines(region):
    return np.all(region.image, axis = 0).sum()

def count_lgr_vlines(region):
    x = region.image.mean(axis =0 ) ==1
    return np.sum(x[:len(x)//2])-1>np.sum(x[len(x)//2:])

def extractor(region):
    area = region.area / region.image.size
    cx, cy = region.centroid_local
    cy /= region.image.shape[0]
    cx /= region.image.shape[1]
    perimeter = region.perimeter / region.image.size
    eccen = region.eccentricity
    vline= count_lgr_vlines(region)
    euler = region.euler_number
    solidity = region.solidity
    elongation = region.image.shape[0]/region.image.shape[1]
    lt = np.sum(region.image[:2, :2])/4
    lb = np.sum(region.image[-2:, :2])/4
    rt = np.sum(region.image[:2, -2:])/4
    rb = np.sum(region.image[-2:, -2:])/4
    return np.array([area, cy, cy>0.56, cx, elongation, perimeter,vline, eccen, solidity, 0.7*euler,lt, lb, rt, rb])

def norm_l1(v1, v2):
    return ((v1 - v2) ** 2).sum() ** 0.5

def classificator(v, templates):
    result = "_"
    min_dist = 10 ** 16
    for key in templates:
        d = norm_l1(v, templates[key])
        if d < min_dist:
            result = key
            min_dist = d
    return result

alphabet = plt.imread("alphabet.png")[:, :, :-1]

gray = alphabet.mean(axis=2)
binary = gray > 0
labeled = label(binary)
regions = regionprops(labeled)

symbols = plt.imread("alphabet-small.png")[:, :, :-1]
gray = symbols.mean(axis=2)
binary = gray < 1
slabeled = label(binary)
sregions = regionprops(slabeled)

templates = {"A": extractor(sregions[2]),
             "B": extractor(sregions[3]), 
             "8": extractor(sregions[0]), 
             "0": extractor(sregions[1]), 
             "1": extractor(sregions[4]), 
             "W": extractor(sregions[5]), 
             "X": extractor(sregions[6]), 
             "*": extractor(sregions[7]),
             "-": extractor(sregions[9]), 
             "/": extractor(sregions[8])}

result = {}
# out_path = Path(__file__).parent/"out"
# out_path.mkdir(exist_ok=True)
for i,region in enumerate(regions):
    # print(f"{i+1}/{len(regions)}")
    v = extractor(region)
    symbol = classificator(v, templates)
    result[symbol] = result.get(symbol, 0) + 1
    # if symbol== "/":
    #     plt.cla()
    #     plt.title(symbol + str(v[9:]))
    #     plt.imshow(region.image)
    #     plt.savefig(out_path/f"{i:03d}.png")

print(result)

