"""
Use the pdfimages command in a Linux terminal to extract images from
PDFs.

Example:
pdfimages file.pdf -all savename
"""

from PIL import Image


class MultiCardImage:
    def __init__(self, card_dim, rows, cols, start=(0, 0), gap=(0, 0), order='row', rev_row=False, rev_col=False):
        self.card_dim = card_dim
        self.rows = rows
        self.cols = cols
        self.start = start
        self.gap = gap
        self.order = order
        self.rev_row = rev_row
        self.rev_col = rev_col

    def slice_file(self, input_file, output):
        filename = input_file[input_file.rfind('/') + 1:]
        filename = filename[:filename.rfind('.')]
        im = Image.open(input_file)
        row_range = range(self.rows)
        col_range = range(self.cols)
        if self.rev_row:
            row_range = list(reversed(row_range))
        if self.rev_col:
            col_range = list(reversed(col_range))
        if output[:-1] != "/":
            output += "/"

        n = 0
        if self.order == 'col':
            for c in col_range:
                for r in row_range:
                    left = self.start[0] + (self.card_dim[0] + self.gap[0]) * c
                    right = left + self.card_dim[0]
                    top = self.start[1] + (self.card_dim[1] + self.gap[1]) * r
                    bottom = top + self.card_dim[1]
                    im1 = im.crop((left, top, right, bottom))
                    n += 1
                    im1.save("{}{}_{}.png".format(output, filename, f'{n:03}'))
        elif self.order == 'row':
            for r in row_range:
                for c in col_range:
                    left = self.start[0] + (self.card_dim[0] + self.gap[0]) * c
                    right = left + self.card_dim[0]
                    top = self.start[1] + (self.card_dim[1] + self.gap[1]) * r
                    bottom = top + self.card_dim[1]
                    im1 = im.crop((left, top, right, bottom))
                    n += 1
                    im1.save("{}{}_{}.png".format(output, filename, f'{n:03}'))
        else:
            raise Exception("`order` must be 'row' or 'col'")
        return None
