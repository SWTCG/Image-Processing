import numpy as np
from PIL import Image


def rgb_to_hcy(rgb_arr):
    """
    Convert image from the red (R), green (G), blue (B) color space to the hue (H), chroma (C), luma (Y) color space.
    :param rgb_arr: a uint8 numpy array with shape (N, M, 3), where N is the image height and M is the width.
    :return: a (N, M, 3) numpy array in the HCY color space
    """
    # Convert 8-bit values to floating point
    rgb_arr = rgb_arr / 255
    red = rgb_arr[:, :, 0]
    green = rgb_arr[:, :, 1]
    blue = rgb_arr[:, :, 2]
    chroma = np.max(rgb_arr, axis=2) - np.min(rgb_arr, axis=2)
    luma = 0.30 * red + 0.59 * green + 0.11 * blue
    hue = np.zeros(red.shape)
    red_is_max = (red == np.max(rgb_arr, axis=2)) & (chroma > 0)
    green_is_max = (green == np.max(rgb_arr, axis=2)) & (chroma > 0)
    blue_is_max = (blue == np.max(rgb_arr, axis=2)) & (chroma > 0)
    hue[red_is_max] = 60 * (green[red_is_max] - blue[red_is_max]) / chroma[red_is_max]
    hue[green_is_max] = 60 * (2 + (blue[green_is_max] - red[green_is_max]) / chroma[green_is_max])
    hue[blue_is_max] = 60 * (4 + (red[blue_is_max] - green[blue_is_max]) / chroma[blue_is_max])
    hue[hue < 0] += 360
    return np.stack((hue, chroma, luma), axis=2)


def hcy_to_rgb(hcy_arr):
    """
    Convert image from the hue (H), chroma (C), luma (Y) color space to the red (R), green (G), blue (B) color space.
    :param hcy_arr: a numpy array with shape (N, M, 3), where N is the image height and M is the width.
    :return: a (N, M, 3) uint8 numpy array in the RGB color space
    """
    hue = hcy_arr[:, :, 0]
    chroma = hcy_arr[:, :, 1]
    luma = hcy_arr[:, :, 2]
    hue_prime = hue / 60
    X = chroma * (1 - np.abs(np.mod(hue_prime, 2) - 1))
    red_1 = np.zeros(hcy_arr.shape[:2])
    green_1 = np.zeros(hcy_arr.shape[:2])
    blue_1 = np.zeros(hcy_arr.shape[:2])

    red_1[(hue_prime >= 0) & (hue_prime <= 1)] = chroma[(hue_prime >= 0) & (hue_prime <= 1)]
    green_1[(hue_prime >= 0) & (hue_prime <= 1)] = X[(hue_prime >= 0) & (hue_prime <= 1)]

    red_1[(hue_prime > 1) & (hue_prime <= 2)] = X[(hue_prime > 1) & (hue_prime <= 2)]
    green_1[(hue_prime > 1) & (hue_prime <= 2)] = chroma[(hue_prime > 1) & (hue_prime <= 2)]

    blue_1[(hue_prime > 2) & (hue_prime <= 3)] = X[(hue_prime > 2) & (hue_prime <= 3)]
    green_1[(hue_prime > 2) & (hue_prime <= 3)] = chroma[(hue_prime > 2) & (hue_prime <= 3)]

    blue_1[(hue_prime > 3) & (hue_prime <= 4)] = chroma[(hue_prime > 3) & (hue_prime <= 4)]
    green_1[(hue_prime > 3) & (hue_prime <= 4)] = X[(hue_prime > 3) & (hue_prime <= 4)]

    blue_1[(hue_prime > 4) & (hue_prime <= 5)] = chroma[(hue_prime > 4) & (hue_prime <= 5)]
    red_1[(hue_prime > 4) & (hue_prime <= 5)] = X[(hue_prime > 4) & (hue_prime <= 5)]

    blue_1[(hue_prime > 5) & (hue_prime <= 6)] = X[(hue_prime > 5) & (hue_prime <= 6)]
    red_1[(hue_prime > 5) & (hue_prime <= 6)] = chroma[(hue_prime > 5) & (hue_prime <= 6)]

    m = luma - (0.3 * red_1 + 0.59 * green_1 + 0.11 * blue_1)
    rgb_arr = (np.stack((red_1 + m, green_1 + m, blue_1 + m), axis=2) * 255).round()
    rgb_arr = rgb_arr.round()
    rgb_arr[rgb_arr > 255] = 255
    rgb_arr[rgb_arr < 0] = 0
    return rgb_arr.astype('uint8')


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


def invert_idc_layers(file):
    """
    Inverts the IDC luminosity and color layers to return the original, untouched image (subject to rounding errors)
    :param file: path to the image file with IDC luminosity and color layers applied
    :return: PIL Image with the luminosity and color layers removed.
    """
    luminosity_layer = np.array([[[99, 99, 99]]])
    luminosity_opacity = 0.08
    color_layer = np.array([[[96, 96, 96]]])
    color_opacity = 0.26

    im = Image.open(file)
    visible_image = np.array(im)

    luminosity_layer_hcy = rgb_to_hcy(luminosity_layer)
    color_layer_hcy = rgb_to_hcy(color_layer)

    idc_luminosity = rgb_to_hcy(visible_image)
    idc_luminosity[:, :, 2] = luminosity_layer_hcy[:, :, 2]
    idc_luminosity = hcy_to_rgb(idc_luminosity)
    real_image = invert_opacity(visible_image, idc_luminosity, luminosity_opacity)

    idc_color = rgb_to_hcy(real_image)
    idc_color[:, :, 0] = color_layer_hcy[:, :, 0]
    idc_color[:, :, 1] = color_layer_hcy[:, :, 1]
    idc_color = hcy_to_rgb(idc_color)
    real_image = invert_opacity(real_image, idc_color, color_opacity)

    return Image.fromarray(real_image)
