import os

from PIL import Image

from concat_images import concat_images


def add_end_slash(path):
    """
    Adds ending forward slash to a path string if it doesn't already end with one.
    """
    if path[-1] != '/':
        path += '/'
    return path


# Image files in `path_to_images` must be named so that each consecutive pair
# of images match together to create the whole card.
path_to_images = "D:/VirtualBox VMs/Shared/images/16_BOH"
save_loc = "D:/Matt/Games/Star Wars TCG/IDC/06 Battle of Hoth/whole/"

path_to_images = add_end_slash(path_to_images)
save_loc = add_end_slash(save_loc)

image_list = [f for f in os.listdir(path_to_images) if f.endswith('.jpg') or f.endswith('.png')]
if len(image_list) % 2 != 0:
    raise Exception("Path to images contains an odd number of image files.")
n = 1
i = 0
while i <= len(image_list) - 1:
    half1 = Image.open(path_to_images + image_list[i])
    half2 = Image.open(path_to_images + image_list[i + 1])
    whole_card = concat_images(half1, half2)
    whole_card.save("{}{}.png".format(save_loc, f'{n:03}'))
    n += 1
    i += 2
