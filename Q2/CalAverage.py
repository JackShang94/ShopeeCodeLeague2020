import cv2
import numpy as np
from matplotlib import pyplot as plt
import os
import fnmatch
from statistics import mean


def find_files(directory, pattern):
    """
    Method to find target files in one directory, including subdirectory
    :param directory: path
    :param pattern: filter pattern
    :return: target file path
    """
    for root, dirs, files in os.walk(directory):
        # Comment out code is to get 10% of each folder
        file_num = len(files) 
        pick_num = file_num // 10
        counter = 0
        for basename in files:
            counter += 1
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                yield filename
            
            if counter >= pick_num:
                print(root)
                break


# path = "/Users/jack/Documents/PythonProjects/ShopeeCodeLeague2020/Q2/dataset/shopee-product-detection-dataset/test/"
path = "/Users/jack/Documents/PythonProjects/ShopeeCodeLeague2020/Q2/dataset/shopee-product-detection-dataset/train/"
# path = "/Users/jack/Documents/PythonProjects/ShopeeCodeLeague2020/Q2/dataset/shopee-product-detection-dataset/train/train/00/"
counter = 0
image_list = []
mean_list = []
stddv_list = []

for filename in find_files(path, '*.jpg'):
    counter += 1
    img = cv2.imread(filename, -1)
    image_list.append(img.shape[:2])

    mean = cv2.mean(img)[0]
    mean_list.append(mean)

    (mean , std) = cv2.meanStdDev(img)
    stddv_list.append(std)

    if (counter % 100 == 0):
        print('number: ' + str(counter))

# avg = [float(sum(col))/len(col) for col in zip(*image_list)]
# print("Size is : "+str(avg))

avg =  np.mean(mean_list)
print("Mean is : "+str(avg))

avg = [float(sum(col))/len(col) for col in zip(*stddv_list)]
print("Std is : "+str(avg))
