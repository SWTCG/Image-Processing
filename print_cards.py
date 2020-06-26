import numpy as np
from PIL import Image

import colorspace


def invert_opacity(result_image, top_image, opacity):
    """
    Inverts the effect of layering an image with opacity < 100% over a second image.
    :param result_image: numpy array with dimensions (N, M, 3), where N is the image height and M is the width,
    representing the color values of the layered, visible image.
    :param top_image: numpy array with dimensions (N, M, 3), where N is the image height and M is the width,
    representing the color values of the top image at 100% opacity.
    :param opacity: a float in the range [0, 1) representing the level of opacity of `top_image`
    :return: numpy array with dimensions (N, M, 3) representing the color values of the bottom image before the top
    opacity layer was applied
    """
    original_image = (result_image - opacity * top_image) / (1 - opacity)
    original_image = original_image.round()
    original_image[original_image > 255] = 255
    original_image[original_image < 0] = 0
    return original_image.astype('uint8')


def invert_idc_layers(image):
    """
    Inverts the IDC luminosity and color layers to return the original,
    untouched image (subject to rounding errors)
    :param image: PIL Image with IDC luminosity and color layers applied
    :return: PIL Image with the luminosity and color layers removed.
    """
    luminosity_layer = np.array([[[99, 99, 99]]])
    luminosity_opacity = 0.08
    color_layer = np.array([[[96, 96, 96]]])
    color_opacity = 0.26

    visible_image = np.array(image)

    luminosity_layer_hcy = colorspace.rgb_to_hcy(luminosity_layer)
    color_layer_hcy = colorspace.rgb_to_hcy(color_layer)

    idc_luminosity = colorspace.rgb_to_hcy(visible_image)
    idc_luminosity[:, :, 2] = luminosity_layer_hcy[:, :, 2]
    idc_luminosity = colorspace.hcy_to_rgb(idc_luminosity)
    real_image = invert_opacity(visible_image, idc_luminosity, luminosity_opacity)

    idc_color = colorspace.rgb_to_hcy(real_image)
    idc_color[:, :, 0] = color_layer_hcy[:, :, 0]
    idc_color[:, :, 1] = color_layer_hcy[:, :, 1]
    idc_color = colorspace.hcy_to_rgb(idc_color)
    real_image = invert_opacity(real_image, idc_color, color_opacity)

    return Image.fromarray(real_image)


def cover_corners(image, long_edge=2100):
    """
    Put black squares on the corners of the image.
    :param image: PIL Image with rounded corners
    :param long_edge: length of the longer edge of the card in pixels. Used for
    determining the size of the black squares to place over corners.
    :return: PIL Image with covered corners
    """
    image = np.array(image)
    scale_ratio = long_edge / 2100
    image[:int(75 * scale_ratio), :int(80 * scale_ratio), :] = 0
    image[int(-90 * scale_ratio):, :int(90 * scale_ratio), :] = 0
    image[int(-90 * scale_ratio):, int(-90 * scale_ratio):, :] = 0
    image[:int(80 * scale_ratio), int(-80 * scale_ratio):, :] = 0
    return Image.fromarray(image)


def remove_art_credit(image):
    """
    Place black rectangle over artist credit.
    """
    if image.width < image.height:
        image = np.array(image)
        image[850:1401, -65:, :] = 0
    else:
        image = np.array(image)
        image[-60:, 710:1261, :] = 0
    return Image.fromarray(image)


def add_bleed(image, bleed_inches=0.125):
    """
    Add bleed to card image by extending the edge pixel on each side.
    :param image: PIL Image to add bleed to
    :param bleed_inches: amount of bleed to add in inches
    :return: PIL Image with bleed added
    """
    if image.height > image.width:
        long_edge = image.height
    else:
        long_edge = image.width
    ppi = long_edge / 3.46457
    bleed_pixels = round(bleed_inches * ppi)
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
    """
    Rotate image to portrait orientation if it is not portrait already.
    """
    if image.height < image.width:
        return image.transpose(Image.ROTATE_90)
    else:
        return image


def gamma_correction(image, gamma=1.22384):
    """
    Perform gamma correction on input image.
    :param image: PIL Image to gamma correct
    :param gamma: gamma correction parameter. The default value is
    for correcting images designed for 1.8 gamma displays (e.g.
    legacy Mac OS X displays) to be viewed on 2.2 gamma displays
    (internet standard).
    :return: gamma-corrected PIL Image
    """
    im = np.array(image)
    im_gamma = 255.0 * np.divide(im, 255.0)**(1 / gamma)
    return Image.fromarray(np.uint8(im_gamma))
