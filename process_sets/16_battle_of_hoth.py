import os

import numpy as np
from PIL import Image

import invert_idc_layers
from cards import cards_df
from concat_images import concat_images


def concat_pdf_images():
    # Image files in `path_to_images` must be named so that each consecutive pair
    # of images match together to create the whole card.
    path_to_images = "D:/VirtualBox VMs/Shared/images/16_BOH"
    save_loc = "D:/Matt/Games/Star Wars TCG/IDC/06 Battle of Hoth/whole/"

    image_list = [f for f in os.listdir(path_to_images) if f.endswith('.jpg') or f.endswith('.png')]
    if len(image_list) % 2 != 0:
        raise Exception("Path to images contains an odd number of image files.")
    n = 1
    i = 0
    while i <= len(image_list) - 1:
        half1 = Image.open(os.path.join(path_to_images, image_list[i]))
        half2 = Image.open(os.path.join(path_to_images, image_list[i + 1]))
        whole_card = concat_images(half1, half2)
        whole_card.save("{}.png".format(os.path.join(save_loc, f'{n:03}')))
        n += 1
        i += 2
    return None


def fix_redesign():
    path_to_images = "D:/Matt/Games/Star Wars TCG/IDC/Print/16_Battle_of_Hoth/redesigned_jpg"
    save_loc = "D:/Matt/Games/Star Wars TCG/IDC/Print/16_Battle_of_Hoth/redesign/"
    image_list = [f for f in os.listdir(path_to_images) if f.endswith('.jpg')]
    for f in image_list:
        save_name = cards_df[(cards_df['Set'] == 'BOH') & (cards_df['ImageFile'] == f[:-4])]['file_name'].iloc[0]
        im = invert_idc_layers.invert_idc_layers(os.path.join(path_to_images, f))
        im = invert_idc_layers.cover_corners(im)
        im.save(os.path.join(save_loc, save_name))
    return None


def redesign_corners():
    path_to_images = "D:/Matt/Games/Star Wars TCG/IDC/Print/16_Battle_of_Hoth/redesign"
    save_loc = "D:/Matt/Games/Star Wars TCG/IDC/Print/16_Battle_of_Hoth/redesign/"
    image_list = [f for f in os.listdir(path_to_images) if f.endswith('.png')]
    for f in image_list:
        im = Image.open(os.path.join(path_to_images, f))
        im = np.array(im)
        im[:75, :80, :] = 0
        im[:85, :20, :] = 0
        Image.fromarray(im).save(os.path.join(save_loc, f))
    return None
