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
    rod_writer.writerow(['Settings', 'Read-Out-Noise', 'Error'])
    i = 0
    for filename in os.listdir(path):
        print(len(os.listdir(path))-i)
        x = image.series_noise(path + filename)
        rod_writer.writerow([filename, x[0], x[1]])
