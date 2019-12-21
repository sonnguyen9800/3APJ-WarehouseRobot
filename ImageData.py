import logging
import os
import sys
from collections import Counter

import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
from skimage.color import rgb2lab, deltaE_cie76
from sklearn.cluster import KMeans

class_counter = 0

image = None
image_path = None
foreground = None
color = None
extracted_image = None


# Convert image to different color space
def convertTo(image, flag=cv.COLOR_RGB2BGR):
    logging.info("Converting Image to {}".format(str(flag)))
    return cv.cvtColor(image, flag)

# Convert Extracted Image to different color space
def convertForegroundTo(self, flag=cv.COLOR_RGB2BGR):
    logging.info("Converting Image to {}".format(str(flag)))
    return cv.cvtColor(self.extracted_image, flag)


# Extracting the foreground, return the image after the extraction finished
def extractForeground(image, times=5, flag=cv.GC_INIT_WITH_RECT, display_image=False):
    logging.info("Extracting foreground with {}".format(times))
    img = image
    mask = np.zeros(img.shape[:2], np.uint8)

    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)
    width, height = img.shape[:2]

    rect = (0, 0, width - 1, height - 1)
    cv.grabCut(img, mask, rect, bgdModel, fgdModel, times, flag)
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
    img = img * mask2[:, :, np.newaxis]

    if display_image == True:
        cv.imshow("Extracted Foreground", img)
        cv.waitKey(0)
        cv.destroyAllWindows()
    return img.astype('uint8')


# Show image on new Window by OpenCV
def showImage(image, image_path):
    logging.info("Show Image {}".format(image_path))
    cv.imshow(str(image_path), image)
    cv.waitKey(0)
    cv.destroyAllWindows()


# save to folder
def saveImage(image, path, name):
    print("SaveImage: Writing to {}, filename: {}".format(path, name))
    cv.imwrite(os.path.join(path, name), image)


def RGB2HEX(color):
    return "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))

def get_colors(image, image_path, num_colors=1, flag_pie=False, imagesize=(600, 400)):
    logging.info("Getting Image's main {} colors from {}".format(num_colors, image_path))
    # image = self.convertTo()
    image = convertForegroundTo(image)

    modified_image = cv.resize(image, imagesize, interpolation=cv.INTER_AREA)
    modified_image = modified_image.reshape(modified_image.shape[0] * modified_image.shape[1], 3)
    t = num_colors + 1
    clf = KMeans(n_clusters=t)
    labels = clf.fit_predict(modified_image)

    counts = Counter(labels)
    center_colors = clf.cluster_centers_
    # We get ordered colors by iterating through the keys
    ordered_colors = [center_colors[i] for i in counts.keys()]

    hex_colors = [RGB2HEX(ordered_colors[i]) for i in counts.keys()]
    rgb_colors = [ordered_colors[i] for i in counts.keys()]

    if (flag_pie):
        plt.pie(counts.values(), labels=hex_colors, colors=hex_colors)
        plt.show()

    count_black = -1
    times = 0
    # print("Count Black: {}".format(count_black))

    for i in rgb_colors:
        count_black += 1

        # print("Loop {}".format(count_black))
        if RGB2HEX(i) == '#000000':
            times += 1
            # print("Count Black {}".format(count_black))
            break

    rgb_colors.pop(count_black)
    return rgb_colors


def match_image_by_color(self, color, number_of_colors=3):
    logging.info("Calculating the difference to the predefined color".format(self.image_path))
    image_colors = self.get_colors(number_of_colors, False)
    selected_color = rgb2lab(np.uint8(np.asarray([[color]])))

    diff_list = []

    for i in range(number_of_colors):
        curr_color = rgb2lab(np.uint8(np.asarray([[image_colors[i]]])))
        diff = deltaE_cie76(selected_color, curr_color)
        diff_list.append(diff)

    if len(diff_list) == 0:
        return 9999

    # print("Minimum Difference: {}".format(min(diff_list)))
    return min(diff_list)


def show_selected_images(self, colorset: dict, output: dict):
    # print(output.__getitem__())
    count = 0
    potential_candidate = 0
    min = sys.maxsize
    for color_picked in colorset:
        diff = self.match_image_by_color(colorset[color_picked])
        if diff < min:
            min = diff
            count += 1
            potential_candidate = color_picked

    ImageObject.class_counter += 1
    self.saveImage(output.get(potential_candidate), "NEW" + str(self.class_counter) + ".jpg")
    # print("Save Image to  {}".format("NEW" + str(self.class_counter) +"jpg"))


if __name__ == '__main__':
    IMAGE_PATH = "image.jpg"

    image = cv.imread(IMAGE_PATH)

