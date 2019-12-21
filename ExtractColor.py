import logging
import os
import sys
from collections import Counter

import cv2 as cv2
import matplotlib.pyplot as plt
import numpy as np
from skimage.color import rgb2lab, deltaE_cie76
from sklearn.cluster import KMeans

IMAGE_PATH = "image.jpg"

COLOR_SET = {
     'RED': [255, 0, 0],
    'ORANGE': [255, 165, 0],
    'INDIGO': [75, 0, 130],
    'VIOLET': [127, 0, 255],
    'GREEN': [0, 128, 0],
    'YELLOW': [255, 255, 0],
    'BLUE': [0, 0, 255]
}


def extractForeground(image, times=10, flag=cv2.GC_INIT_WITH_RECT, display_image=False):
    logging.info("Extracting foreground with {}".format(times))

    img = image
    mask = np.zeros(img.shape[:2], np.uint8)

    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)

    width, height = img.shape[:2]

    rect = (0, 0, width - 1, height - 1)
    cv2.grabCut(img, mask, rect, bgdModel, fgdModel, times, flag)
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
    img = img * mask2[:, :, np.newaxis]

    if display_image == True:
        cv2.imshow("Extracted Foreground", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return img.astype('uint8')


def convertForegroundTo(image, flag=cv2.COLOR_RGB2BGR):
    logging.info("Converting Image to {}".format(str(flag)))
    return cv2.cvtColor(image, flag)


def RGB2HEX(color):
    return "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))


def get_colors(image, num_colors=1, flag_pie=False, imagesize=(600, 400)):
    # image = self.convertTo()
    image = image

    modified_image = cv2.resize(image, imagesize, interpolation=cv2.INTER_AREA)
    modified_image = modified_image.reshape(modified_image.shape[0] * modified_image.shape[1], 3)

    t = num_colors
    clf = KMeans(n_clusters=t)
    labels = clf.fit_predict(modified_image)

    counts = Counter(labels)

    print("Count Values" + str(counts.values))

    for i in counts.values():
        print(i)

    center_colors = clf.cluster_centers_
    # We get ordered colors by iterating through the keys
    ordered_colors = [center_colors[i] for i in counts.keys()]
    hex_colors = [RGB2HEX(ordered_colors[i]) for i in counts.keys()]
    rgb_colors = [get_colors_name(ordered_colors[i], COLOR_SET) for i in counts.keys()]

    if (flag_pie):
        plt.pie(counts.values(), labels=rgb_colors, colors=hex_colors)
        plt.show()


    return rgb_colors

# Take an RGB code, get the name of that color
def get_colors_name(color_extracted, ColorSet: dict):
    selected_colors = ""
    min_diff = 9999
    color_extracted_lab = rgb2lab(np.uint8(np.asarray([[color_extracted]])))
    for color_sample in ColorSet:
        color_sample_lab = rgb2lab(np.uint8(np.asarray([[ColorSet[color_sample]]])))
        color_diff = deltaE_cie76(color_extracted_lab, color_sample_lab)
        if min_diff >= color_diff:
            min_diff = color_diff
            selected_colors = color_sample
    return selected_colors

if __name__ == '__main__':
    image = cv2.imread(IMAGE_PATH)
    image_foreground = extractForeground(image, display_image=True)

    image_converted = convertForegroundTo(image)

    colors_assigned = get_colors(image_converted, flag_pie=True)
    print(colors_assigned)