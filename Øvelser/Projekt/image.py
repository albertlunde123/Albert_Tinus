import numpy as np
from PIL import Image
from numba import jit

path = "../../../Data_DC/"
qualities = ["Low Noise", "High Capacity"]
speeds = ["100 kHz", "1 MHz", "4 MHz"]
gains = ["Low", "Medium", "High"]
bins = ["1x1","4x4","8x8","20x20"]

#Laver en string som er den komplette path der skal åbnes

def name(path, quality, gain, bins, read_out_rate):
    result = "ron_"

    if(quality == "Low Noise"):
        result += "qL_"
    else:
        result += "qH_"

    if(gain == "Low"):
        result += "gL_"
    if(gain == "Medium"):
        result += "gM_"
    if(gain == "High"):
        result += "gH_"

    if(bins == "1x1"):
        result += "b1_"
    if(bins == "4x4"):
        result += "b4_"
    if(bins == "8x8"):
        result += "b8_"
    if(bins == "20x20"):
        result += "b20_"

    if(read_out_rate == "100 kHz"):
        result += "r0.1"
    if(read_out_rate == "1 MHz"):
        result += "r1"
    if(read_out_rate == "4 MHz"):
        result += "r4"

    result += ".tif"

    return path + result

#Autogenerer en path for alle kombinationer af indstillinger

def files(qualities, gains, bins, speeds):
    files = []
    for q in qualities:
        for g in gains:
            for b in bins:
                for s in speeds:
                    files.append(name(path,q,g,b,s))
    return files

def tif_unfold(image):

    pics = []

    for i in range(image.n_frames):
        image.seek(i)
        pics.append(np.array(image, dtype = np.float64))

    return pics

def read_out_noise(image1, image2):
    return np.std((image1 - image2).ravel())/np.sqrt(2)

def series_noise(path):

    factor = int(path.split('b')[-1].split('_')[0])**2

    pics = tif_unfold(Image.open(path))
    diff_ims = []

    for i in range(len(pics) - 1):
        diff_ims.append(read_out_noise(pics[i], pics[i+1]))

    diff_ims = np.array(diff_ims)

    return [np.mean(diff_ims), np.std(diff_ims, ddof = 1)/np.sqrt(len(pics))]



# def stds(pics):
#     stds = []
#     j = len(pics[0])
#     for i in range(len(pics[0])):
#         stds.append([np.std([pic[i] for pic in pics], ddof = 1)])
#         j = j - 1
#         print(j)
#     return np.array(stds)

# np.array(pics)


def dark_mean(path):
    pics = tif_unfold(Image.open(path))
    piccers = [pic.ravel() for pic in pics]

    means = np.zeros(len(piccers[0]))
    for i in range(len(piccers)):
        means += piccers[i]
    means = means/10
    std = np.std(pics, axis = 2, ddof = 1).ravel()

    return sum([np.mean(means)/st**2 for pic,st in zip(pics, std)])/sum(1/std**2), sum(1/std**2)**(-0.5)

# def dark_error(path):
#     pics = tif_unfold(Image.open(path))
#     N = len(pics)
#     pics = [pic.ravel() for pic in pics]
#     stds = [np.std([pic[i] for pic in pics], ddof = 1) for i in range(len(pics[0]))]
#     err_CE = sum(1/stds**2)**(-0.5)
#     return err_CE

