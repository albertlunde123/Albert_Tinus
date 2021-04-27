import numpy as np
from PIL import Image
from numba import jit

path = "../../../Data/"

@jit(nopython = True)
def read_out_noise(image1, image2):
    return np.std(image1 - image2)/np.sqrt(2)

im1 = Image.open(path + 'ron_qH_gH_b1_r0.1.tif')
im1.seek(0)
im2 = Image.open(path + 'ron_qH_gH_b1_r1.tif')
im1 = np.array(im1)
im2 = np.array(im2)

@jit
def fun():
    for i in range(len(im1)):
        for j in range(len(im1)):
            if im1[i,j] < 100:
                print(im1[i,j])

fun()
# print(read_out_noise(im1, im2))
