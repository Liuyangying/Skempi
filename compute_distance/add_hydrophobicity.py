import numpy as np
import pandas as pd



if __name__ == '__main__':


    sheet = pd.read_csv('F:\\PycharmProjects\\combine_sheet\\compute_distance\\add_distance_sheet_add_features.csv', index_col=0)

    amino_acid_size = {'G':60.1,'A':88.6,'S':89.0,'C':108.5,'D':111.1,'P':112.7,'N':114.1,'T':116.1,'E':138.4,'V':140.0,'Q':143.8,
                       'H':153.2,'M':162.9,'I':166.7,'L':166.7, 'K':168.6,'R':173.4,'F':189.9,'Y':193.6,
                       'W':227.8}

    amino_acid_hydrophobicity = {'G': -0.4, 'A': 1.8, 'S': -0.8, 'C': 2.5, 'D': -3.5, 'P': -1.6, 'N': -3.5, 'T': -0.7,
                       'E': -3.5, 'V': 4.2, 'Q': -3.5,'H': -3.2, 'M': 1.9, 'I': 4.5, 'L': 3.8, 'K': -3.9, 'R': -4.5, 'F': 2.8, 'Y': -1.3,
                       'W': -0.9}

    # wild = sheet.iloc[1, 4][0]
    # mutan = sheet.iloc[1, 4][-1]
    for i in range(len(sheet)):
        wild = sheet.iloc[i,4][0]
        mutant = sheet.iloc[i,4][-1]
        sheet.iloc[i,26] = amino_acid_hydrophobicity[wild]
        sheet.iloc[i,27] = amino_acid_hydrophobicity[mutant]
        sheet.iloc[i, 28] = amino_acid_size[wild]
        sheet.iloc[i, 29] = amino_acid_size[mutant]

    sheet.to_csv("sheet_all_features.csv")


    print('yes')