import os

from PIL import Image

import invert_idc_layers


def remove_layers():
    path_to_images = "D:/Matt/Games/Star Wars TCG/IDC/Print/20_Legacy_of_the_Force_Smugglers/alternate"
    save_loc = "D:/Matt/Games/Star Wars TCG/IDC/Print/20_Legacy_of_the_Force_Smugglers/alternate"
    image_list = [f for f in os.listdir(path_to_images) if f.endswith('.jpg')]
    for f in image_list:
        save_name = f[:-4] + '.png'
        im = invert_idc_layers.invert_idc_layers(os.path.join(path_to_images, f))
        im = invert_idc_layers.cover_corners(im)
        im.save(os.path.join(save_loc, save_name))
    return None


def remove_art_credit():
    path_to_images = "D:/Matt/Games/Star Wars TCG/IDC/Print/20_Legacy_of_the_Force_Smugglers/art_credit"
    save_loc = "D:/Matt/Games/Star Wars TCG/IDC/Print/20_Legacy_of_the_Force_Smugglers/creditless"
    image_list = [f for f in os.listdir(path_to_images) if f.endswith('.png')]
    for f in image_list:
        save_name = f[:-4] + '_creditless.png'
        im = Image.open(os.path.join(path_to_images, f))
        im = invert_idc_layers.remove_art_credit(im)
        im.save(os.path.join(save_loc, save_name))
    return None
