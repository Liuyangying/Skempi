# This is a sample Python script.
import pandas as pd
import numpy as np
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    skempi1 = pd.read_excel(
        'Final Integrated Volumes (Skempi Dataset).xlsx', index_col=0)
    skempi2 = pd.read_excel('Copy of skempi_v2(1).xlsx')

    colnames2 = skempi2.columns.values
    skempi1[colnames2] = pd.NaT
    PDB_names = skempi2.iloc[:, 0]

    # unique_PDB = skempi1.iloc[:,0].unique()
    # mutation = skempi1.iloc[:,3]
    # unique_mutation = skempi1.iloc[:,3].unique()
    # mutation_num = []
    # num = 0
    # for i in unique_mutation:
    #     mutation_num.append(len(i.split(',')))
    # mutation_num = list(set(mutation_num))
    #
    # mutation_record = pd.DataFrame(np.empty([len(unique_PDB),len(mutation_num)]),index = unique_PDB, columns = mutation_num )
    for n1 in range(0, len(skempi1.iloc[:,3])):
        skempi1.iloc[n1,3] = ','.join(sorted(skempi1.iloc[n1,3].split(',')))

    for n2 in range(0, len(skempi2.iloc[:,1])):
        skempi2.iloc[n2,1] = ','.join(sorted(skempi2.iloc[n2,1].split(',')))


    for i in range(0, 7085):
        PC = PDB_names[i].split("_")
        for j in range(0, 6169):
            if PC[0] == skempi1.iloc[j, 0] and PC[1] == skempi1.iloc[j, 1] and PC[2] == skempi1.iloc[j, 2] and skempi2.iloc[i, 1] == skempi1.iloc[j, 3]:
                skempi1.iloc[j, 19:48] = skempi2.iloc[i, :]

    skempi1.to_csv('combined.csv')

    print('yes')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
