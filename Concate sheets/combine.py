# This is a sample Python script.
import pandas as pd
import numpy as np


def load_sheet(sheet1, sheet2):
    """
    read intergrated volumns sheet and Skempi_2.0 sheet
    :param sheet1:
    :param sheet2:
    :return:
    """

    skempi1 = pd.read_excel(sheet1, index_col=0)
    skempi2 = pd.read_excel(sheet2)

    colnames2 = skempi2.columns.values
    skempi1[colnames2] = pd.NaT

    for n1 in range(0, len(skempi1.iloc[:,3])):
        skempi1.iloc[n1,3] = ','.join(sorted(skempi1.iloc[n1,3].split(',')))

    for n2 in range(0, len(skempi2.iloc[:,1])):
        skempi2.iloc[n2,1] = ','.join(sorted(skempi2.iloc[n2,1].split(',')))

    return skempi1, skempi2


def combine(skempi1, skempi2):
    """

    :param skempi1:
    :param skempi2:
    :return:
    """

    PDB_names = skempi2.iloc[:, 0]

    for i in range(0, 7085):
        PC = PDB_names[i].split("_")
        for j in range(0, 6169):
            if PC[0] == skempi1.iloc[j, 0] and PC[1] == skempi1.iloc[j, 1] and PC[2] == skempi1.iloc[j, 2] and skempi2.iloc[i, 1] == skempi1.iloc[j, 3]:
                skempi1.iloc[j, 19:48] = skempi2.iloc[i, :]

    skempi1.to_csv('combined1.csv')



if __name__ == '__main__':

    sheet1 = 'Final Integrated Volumes (Skempi Dataset).xlsx'
    sheet2 = 'Copy of skempi_v2(1).xlsx'
    skempi1, skempi2 = load_sheet(sheet1, sheet2)
    combine(skempi1, skempi2)



    print('yes')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
