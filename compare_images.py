import numpy as np
from PIL import Image

file1 = "D:/Matt/Games/Star Wars TCG/WotC/Scans/02 Sith Rising/backup/Sith_Rising001.tif"
file2 = "D:/Matt/Games/Star Wars TCG/WotC/Scans/02 Sith Rising/Sith_Rising001.tif"
im1 = np.array(Image.open(file1))
im2 = np.array(Image.open(file2))

if im1.shape != im2.shape:
    print("Image dimensions do not match.")
    print("Image 1: {} x {}, {} channels".format(im1.shape[0], im1.shape[1], im1.shape[2]))
    print("Image 2: {} x {}, {} channels".format(im2.shape[0], im2.shape[1], im2.shape[2]))
else:
    match = np.all(im1 == im2)
    if match:
        print("Images match")
    else:
        max_diff = np.max(abs(im1.astype('int') - im2.astype('int')))
        num_diff = len(im1[im1 != im2])
        print("Images do not match")
        #print("Number of differences: {} ({}%)".format(num_diff, round(num_diff / np.prod(im1.shape), 2)))
        print("Maximum difference: {}".format(max_diff))
