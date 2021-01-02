import os

from PIL import Image

import print_cards

path_to_images = './images'  # Replace this with the path to the directory containing your images.
output_directory = './output'  # Replace this with the directory where you want the modified images to be saved.

# Loop through image files in the directory
for file in os.listdir(path_to_images):
    if file.endswith(('.jpg', '.png', '.tif')):
        image = Image.open(os.path.join(path_to_images, file))

        # Remove IDC layers
        image = print_cards.invert_idc_layers(image)

        # Cover corners
        image = print_cards.cover_corners(image)

        # Remove art credit. This is optional, and to my knowledge this is only
        # applicable for cards from the Legacy of the Force: Smugglers
        # expansion
        image = print_cards.remove_art_credit(image)

        # Add bleed to the edges of the card. The default bleed amount is
        # 1/8 inch.
        image = print_cards.add_bleed(image, 0.125)

        # Apply gamma correction. The default gamma correction is 1.22384
        # and is intended to correct images encoded with gamma=1.8 for viewing
        # on 2.2 gamma displays.
        image = print_cards.gamma_correction(image, 1.22384)

        # Rotate images so they are in portrait
        image = print_cards.set_portrait(image)

        # Save modified image. I save as .png to avoid generation loss.
        save_name = file[:file.rfind('.')] + '.png'
        image.save(os.path.join(output_directory, save_name))
