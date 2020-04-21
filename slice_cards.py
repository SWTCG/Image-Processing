from PIL import Image


def slice_file(input_file, output, card_dim, rows, cols, rev_row=False, rev_col=False):
    filename = input_file[input_file.rfind('/') + 1:]
    filename = filename[:filename.rfind('.')]
    im = Image.open(input_file)
    row_range = range(rows)
    col_range = range(cols)
    if rev_row:
        row_range = list(reversed(row_range))
    if rev_col:
        col_range = list(reversed(col_range))
    if output[:-1] != "/":
        output += "/"

    n = 0
    for c in col_range:
        for r in row_range:
            left = card_dim[0] * c
            right = card_dim[0] * (c + 1)
            top = card_dim[1] * r
            bottom = card_dim[1] * (r + 1)
            im1 = im.crop((left, top, right, bottom))

            n += 1
            im1.save("{}{}_{}.png".format(output, filename, f'{n:03}'))
    return None
