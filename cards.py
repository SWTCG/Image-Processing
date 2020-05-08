import os

import numpy as np
import pandas as pd
from PIL import Image


cards_df = pd.read_csv(os.path.join(os.path.dirname(__file__), 'AllSets.txt'),
                       sep='\t', encoding='latin', usecols=list(range(14)))
cards_df['Number'] = pd.to_numeric(cards_df['Number'], errors='ignore')

# Set file extensions. Every set is .png except for the first 4 IDC sets which
# could be extracted directly as .jpg from the PDFs.
cards_df['file_extension'] = '.png'
cards_df.loc[cards_df['Set'].isin(['FOTR', 'SAV', 'BOE', 'RAW']), 'file_extension'] = '.jpg'

chars_to_replace = r"[ '!@#$%^&*\[\]{};:,./<>\?\\|`\~\-=+\"]"
cards_df['file_name'] = (cards_df['Name']
                         .str.replace(r'[()]', '')
                         .str.replace(chars_to_replace, '_')
                         .str.replace(r'(_)\1{%d,}' % 1, r'\1'))
cards_df['file_name'] = (
        cards_df['Set']
        + cards_df['Number'].str.replace('S', 'sub').str.replace('P', 'promo').str.zfill(3)
        + '_'
        + cards_df['file_name']
        # + cards_df['file_extension']
)
landscape_types = ['Equipment', 'Battle', 'Location', 'Mission', 'Resource']
cards_df['landscape'] = np.where(cards_df['Type'].isin(landscape_types), True, False)


def ordered_rename(directory, expansion):
    # Files in directory MUST be in the same order as the list of names.
    exts = tuple(cards_df[cards_df['Set'] == expansion]['file_extension'].unique())
    file_list = [f for f in os.listdir(directory) if f.endswith(exts)]
    file_list.sort()
    name_list = (cards_df[(cards_df['Set'] == expansion) & (cards_df['Rarity'] != 'P')]
                 .sort_values('file_name')['file_name'])
    if len(file_list) == len(name_list):
        for i in range(len(file_list)):
            ext = file_list[i][file_list[i].rfind('.'):]
            os.rename(os.path.join(directory, file_list[i]), os.path.join(directory, name_list.iloc[i] + ext))
    else:
        raise Exception("Number of files to be renamed does not equal the number of names.")
    return None


def rotate(directory, ccw_rotations):
    if ccw_rotations % 4 == 0:
        return None
    elif ccw_rotations % 4 == 1:
        rotation = Image.ROTATE_90
    elif ccw_rotations % 4 == 2:
        rotation = Image.ROTATE_180
    elif ccw_rotations % 4 == 3:
        rotation = Image.ROTATE_270
    else:
        raise Exception("Invalid value of `ccw_rotations`.")

    for file in os.listdir(directory):
        if file[:file.rfind('.')] in cards_df[~cards_df['landscape']]['file_name'].values:
            im = Image.open(os.path.join(directory, file))
            im.transpose(rotation).save(os.path.join(directory, file))
    return None
