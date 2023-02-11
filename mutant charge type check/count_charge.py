import numpy as np
import pandas as pd

def load(path):

    combined = pd.read_csv(path, index_col=0)
    PDB_Chain = [list(i) for i in list(zip(combined.loc[:, "PDBCode"], combined.loc[:, "Chain1"], combined.loc[:, "Chain2"]))]
    PDB_Chain_comb = [("_").join(i) for i in PDB_Chain]
    combined.insert(0, "pdb_chain", PDB_Chain_comb)

    return combined

def keep_single(combined):
    """

    :param combined:
    :return:
    """
    index = combined.index.values

    for i in index:
        mut = len(combined.loc[i, 'MutantList'].split(','))
        if mut > 1:
            combined = combined.drop(i)

    combined_single = combined

    return combined_single


def mutant_type(combined_single, sheet):

    if sheet == 'original':
        c = 4
    elif sheet == 'add':
        c = 21

    Pos = ['H','K','R']
    Neg = ['D','E']

    Pos_Neg = 0
    Neg_Pos = 0
    Unchar_Pos = 0
    Unchar_Neg = 0
    Pos_Unchar = 0
    Neg_Unchar = 0

    combined_single['mutant type'] = 0

    for j in range(0, len(combined_single)):
        ori = combined_single.iloc[j, c][0]
        mut = combined_single.iloc[j, c][-1]

        if ori in Pos:
            if mut in Neg:
                Pos_Neg += 1
                combined_single.iloc[j,49] = 'Pos_Neg'
            elif mut not in Neg+Pos:
                Pos_Unchar += 1
                combined_single.iloc[j, 49] = 'Pos_Unchar'
        if ori in Neg:
            if mut in Pos:
                Neg_Pos += 1
                combined_single.iloc[j, 49] = 'Neg_Pos'
            elif mut not in Neg+Pos:
                Neg_Unchar += 1
                combined_single.iloc[j, 49] = 'Neg_Unchar'

        if ori not in Neg+Pos:
            if mut in Pos:
                Unchar_Pos += 1
                combined_single.iloc[j, 49] = 'Unchar_Pos'
            elif mut in Neg:
                Unchar_Neg += 1
                combined_single.iloc[j, 49] = 'Unchar_Neg'


    return Pos_Neg, Neg_Pos, Unchar_Pos, Unchar_Neg, Pos_Unchar, Neg_Unchar


if __name__ == '__main__':

    combined = load('combined.csv')
    combined_single = keep_single(combined)

    Pos_Neg, Neg_Pos, Unchar_Pos, Unchar_Neg, Pos_Unchar, Neg_Unchar = mutant_type(combined_single,'original')

    print(Pos_Neg, Neg_Pos, Unchar_Pos, Unchar_Neg, Pos_Unchar, Neg_Unchar)
    combined_single.to_csv('single charge.csv')
    f = open('mutation type summary.txt','w')
    f.write('Pos_Neg:'+ str(Pos_Neg)+'\n'+
            'Neg_Pos:'+ str(Neg_Pos)+'\n'+
            "Unchar_Pos:"+str(Unchar_Pos)+'\n'+
            "Unchar_Neg:"+str(Unchar_Neg)+'\n'+
            "Pos_Unchar："+ str(Pos_Unchar)+'\n'+
            "Neg_Unchar："+str(Neg_Unchar)+'\n')

    f.close()
    # Pos_Neg, Neg_Pos, Unchar_Pos, Unchar_Neg, Pos_Unchar, Neg_Unchar = mutant_type(combined_single, 'add')
    # print(Pos_Neg, Neg_Pos, Unchar_Pos, Unchar_Neg, Pos_Unchar, Neg_Unchar)

    print('yes')