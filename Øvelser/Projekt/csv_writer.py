import csv
import numpy as np
import os
from PIL import Image
import image

path = '../../../Data/'

# example = '/ron_qH_gH_b1_r0.1.tif'
# print(image.series_noise(path + example))

with open('read-out-noise.csv', mode = 'w') as rod:

    rod_writer = csv.writer(rod, delimiter = ',')
    rod_writer.writerow(['Settings', 'Read-Out-Noise', 'Error'])
    for filename in os.listdir(path):
        x = image.series_noise(path + filename)
        rod_writer.writerow([filename, x[0], x[1]])
