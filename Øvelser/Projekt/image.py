import numpy as np
from PIL import Image
from numba import jit

path = "../../../Data/"

im = Image.open(path + 'ron_qH_gH_b1_r0.1.tif')

def tif_unfold(image):

    pics = []

    for i in range(image.n_frames):
        image.seek(i)
        pics.append(np.array(image, dtype = np.float64))

    return pics

def read_out_noise(image1, image2):
    return np.std((image1 - image2).ravel())/np.sqrt(2)

def series_noise(pics):

    diff_ims = []

    for i in range(len(pics) - 1):
        diff_ims.append(read_out_noise(pics[i], pics[i+1]))

    diff_ims = np.array(diff_ims)

    return [np.mean(diff_ims), np.std(diff_ims, ddof = 1)/np.sqrt(len(pics))]

im = tif_unfold(im)

print(series_noise(im))

