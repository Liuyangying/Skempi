import pandas as pd
import numpy as np

def load(path):

    combined = pd.read_csv(path, index_col=0)
    PDB_Chain = [list(i) for i in list(zip(combined.loc[:, "PDBCode"], combined.loc[:, "Chain1"], combined.loc[:, "Chain2"]))]
    PDB_Chain_comb = [("_").join(i) for i in PDB_Chain]
    combined.insert(0, "pdb_chain", PDB_Chain_comb)

    return combined


def chainpair_mutation(combined, columns):

    #columns= '#Pdb'
    PDB_chain_unique = combined.loc[:, columns].unique()

    if columns == '#Pdb':
        c = 21
        l = 20
    elif columns == 'pdb_chain':
        c = 4
        l = 0

    #mutant_num is number of mutants that all chain-pair could have
    mutant_num = []
    for i in range(0, len(combined)):
        mut = len(combined.iloc[i, c].split(','))
        mutant_num.append(mut)
    mutant_num = set(mutant_num)

    #generate an empty chain-pair and mutation table, columns is muation number, index is chain-pair
    table = pd.DataFrame(columns=mutant_num, index=PDB_chain_unique)

    #write sum of each mutation number for each chain pair
    for pdb in PDB_chain_unique:
        temp = []
        for n in range(0, len(combined)):
            if pdb == combined.iloc[n, l]:
                num = len(combined.iloc[n, c].split(','))
                temp.append(num)
        temp = pd.DataFrame(temp, columns=[pdb])
        temp = temp.groupby([pdb]).size()
        temp = temp.to_frame().transpose()
        temp.index = [pdb]
        for m in temp.columns:
            table.loc[pdb, m] = temp.loc[pdb, m]

    table = table.fillna(0)
    sum = table.sum().sum()

    return table, sum


if __name__ == '__main__':

    combined = load('combined.csv')
    add_table, add_sum = chainpair_mutation(combined, '#Pdb')
    ori_table, ori_sum = chainpair_mutation(combined, 'pdb_chain')

    check = add_table.equals(ori_table)
    print(check)
    print(add_sum == ori_sum)


    print("yes")

