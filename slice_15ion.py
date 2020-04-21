import os

from slice_cards import slice_file

in_dir = "D:/VirtualBox VMs/Shared/images/"
out_dir = "D:/Matt/Games/Star Wars TCG/IDC/Print/15_Invasion_of_Naboo/python"
dim = (964, 1338)
rows = 2
cols = 4

for filename in os.listdir(in_dir):
    if filename.endswith(".jpg"):
        if in_dir[:-1] != "/":
            in_dir += "/"
        slice_file(in_dir + filename, out_dir, dim, rows, cols, rev_row=True)


class MultiCardImage:
    pass
