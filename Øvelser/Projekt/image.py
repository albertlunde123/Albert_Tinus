import numpy as np
from PIL import Image
from numba import jit

path = "../../../Data/"
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

def series_noise(pics):

    diff_ims = []

    for i in range(len(pics) - 1):
        diff_ims.append(read_out_noise(pics[i], pics[i+1]))

    diff_ims = np.array(diff_ims)

    return [np.mean(diff_ims), np.std(diff_ims, ddof = 1)/np.sqrt(len(pics))]

im = tif_unfold(im)


print(series_noise(im))

