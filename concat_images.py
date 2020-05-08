from PIL import Image


def concat_images(image1, image2, mode=None):
    """
    Concatenate two images with the same height or width. If `mode` is not specified, the resulting image will have the
    color mode of `image1`.
    :param image1: The left or top image, depending on if concatenating horizontally or vertically.
    :param image2: The right or bottom image
    :param mode: The color mode of the resulting image.
    :return: concatenated Pillow Image
    """
    if mode is None:
        mode = image1.mode
    if image1.width == image2.width:
        new_image = Image.new(mode, (image1.width, image1.height + image2.height))
        new_image.paste(image1, (0, 0))
        new_image.paste(image2, (0, image1.height))
    elif image1.height == image2.height:
        new_image = Image.new(mode, (image1.width + image2.width, image1.height))
        new_image.paste(image1, (0, 0))
        new_image.paste(image2, (image1.width, 0))
    else:
        raise Exception("Images do not have the same height or width.")

    return new_image
