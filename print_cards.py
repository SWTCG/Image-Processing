import numpy as np
from PIL import Image


def add_bleed(image):
    if image.height > image.width:
        long_edge = image.height
    else:
        long_edge = image.width
    ppi = long_edge / 3.46457
    bleed_pixels = round(0.125 * ppi)
    im = np.array(image)
    sides = {
        'top': np.repeat(im[0:1, :, :], bleed_pixels, axis=0),
        'bottom': np.repeat(im[-1:im.shape[0], :, :], bleed_pixels, axis=0)
    }
    im = np.concatenate((sides['top'], im, sides['bottom']), axis=0)
    sides['left'] = np.repeat(im[:, 0:1, :], bleed_pixels, axis=1)
    sides['right'] = np.repeat(im[:, -1:im.shape[1], :], bleed_pixels, axis=1)
    im = np.concatenate((sides['left'], im, sides['right']), axis=1)
    return Image.fromarray(im)


def set_portrait(image):
    if image.height < image.width:
        return image.transpose(Image.ROTATE_90)
    else:
        return image
