import pandas as pd
import numpy as np


def load(path):

    combined = pd.read_csv(path, index_col=0)
    # PDB_Chain = [list(i) for i in list(zip(combined.loc[:, "PDBCode"], combined.loc[:, "Chain1"], combined.loc[:, "Chain2"]))]
    # PDB_Chain_comb = [("_").join(i) for i in PDB_Chain]
    # combined.insert(0, "pdb_chain", PDB_Chain_comb)

    return combined


def clean_aff_mut(single_sheet):
    """
    This function is used to remove entries that are not float type in Affinity_mut(M) column
    :param sheet:
    :return:
    """
    #aff_mt = single_sheet.iloc[:, -3]

    s = 0
    droplist = []

    for i in range(0, len(single_sheet.index)):

        if ">" in single_sheet.iloc[i,-3]:
            s = s+1
            droplist.append(single_sheet.index[i])
            print(s)
        elif "<" in single_sheet.iloc[i,-3]:
            s = s+1
            droplist.append(single_sheet.index[i])
            print(s)
        elif "n.b" in single_sheet.iloc[i,-3]:
            #print(single_sheet.iloc[i,-3])
            s = s+1
            droplist.append(single_sheet.index[i])
            print(s)
        elif 'unf' in single_sheet.iloc[i,-3]:
            s = s + 1
            droplist.append(single_sheet.index[i])
            print(s)

    # remove the entry , which include special string in Affinity_mut column
    cleansheet = single_sheet.drop(index=droplist)

    # convert the element in certain column to numeric type
    cleansheet['Affinity_mut (M)'] = pd.to_numeric(cleansheet['Affinity_mut (M)'])
    print(s)

    return cleansheet


def clean_temperature(cleansheet):
    '''
    1. This function is to remove (assumed) form record, e.g. 298(assumed)→298
    2. Besides, this function will remove record include 'nan',
    which means delete the row whose Temperature column includes 'nan'
    :param cleansheet:
    :return:
    '''

    s = 0
    droplist = []
    cleansheet['Temperature'] = cleansheet['Temperature'].astype(str)
    for i in range(0, len(cleansheet.index)):
        if "(assumed)" in cleansheet.iloc[i, -1]:
            s = s + 1
            cleansheet.iloc[i, -1] = cleansheet.iloc[i, -1].replace('(assumed)', '')
            # print(cleansheet.iloc[i,-1].replace('(assumed)',''))
            print(cleansheet.iloc[i, -1], cleansheet.index[i])
        elif 'nan' in cleansheet.iloc[i, -1]:
            s = s + 1
            droplist.append(cleansheet.index[i])
            print(i)
    print(droplist)
    cleansheet = cleansheet.drop(index=droplist)
    cleansheet['Temperature'] = pd.to_numeric(cleansheet['Temperature'])

    return cleansheet


if __name__ == '__main__':

    single_sheet = load('F:\PycharmProjects\combine_sheet\\clean_sheet_temp_affi\single_mutant_sheet_2.csv')
    print(len(single_sheet))
    cleansheet = clean_aff_mut(single_sheet)
    cleansheet2 = clean_temperature(cleansheet)
    cleansheet2.to_csv("clean_sheet_temp_affi.csv")

    name = cleansheet.columns

    print("yes")


