import csv
import numpy as np
import os
from PIL import Image
import image

path = '../../../Data_DC/'

# example = '/ron_qH_gH_b1_r0.1.tif'
# print(image.series_noise(path + example))

with open('dark-charge.csv', mode = 'w') as rod:

    rod_writer = csv.writer(rod, delimiter = ',')
    rod_writer.writerow(['Settings', 'Mean-charge', 'Error'])
    i = 0
    for filename in os.listdir(path):
        i += 1
        print(len(os.listdir(path))-i)
        # x = image.series_noise(path + filename)
        x = image.dark_mean(path + filename)
        y = image.dark_error(path + filename)
        rod_writer.writerow([filename, x, y])
