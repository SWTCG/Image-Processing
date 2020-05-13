import numpy as np


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
