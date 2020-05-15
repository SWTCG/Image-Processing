# Image Processing #

This module contains functions to aid in the process of preparing Star Wars TCG images for printing.

### Contents ###

The <code>print_cards.py</code> file contains several functions that perform common print preparation tasks
* <code>invert_idc_layers</code>: The individual .jpg files downloaded from the IDC website are intended for digial use, and as such contain special layers that are intended to simulate the look of a real card on a digital screen. This function removes these layers, as they are not desireable for printing. The printable PDFs do not contain these layers, so if you extract the card images from there, you do not need to use this function. 
* <code>cover_corners</code>: This function covers the rounded corners of the card with black rectangles. Be sure to remove the IDC layers first, if necessary.
* <code>remove_art_credit</code>: A handful of cards in the Legacy of the Force: Smugglers expansion have an artist credit along the card border. If you do not wish to have the artist credit shown, this function will place black rectangles over it. As with the <code>cover_corners</code> function, remove IDC layers first before applying.
* <code>add_bleed</code>: This function will add bleed around the edges of the card by extending each side's edge pixels outwards. The default amount of bleed to add is 1/8 inch. 
* <code>set_portrait</code>: This function will rotate cards shown in landscape orientation to portrait and leave portrait cards untouched.

See <code>example.py</code> for an example of looping through a directory and applying changes to the images.