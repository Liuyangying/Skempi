# This is a sample Python script.
import pandas as pd
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    skempi1 = pd.read_excel('Final Integrated Volumes (Skempi Dataset).xlsx', index_col = 0)
    skempi2 = pd.read_excel('Copy of skempi_v2(1).xlsx')

    colnames2 = skempi2.columns.values
    skempi1[colnames2] = pd.NaT
    PDB_names = skempi2.iloc[:, 0]

    for i in range(0, 7085):
        PC = PDB_names[i].split("_")
        for j in range(0, 6169):
            if PC[0] == skempi1.iloc[j, 0] and PC[1] == skempi1.iloc[j, 1] and PC[2] == skempi1.iloc[j, 2] and skempi2.iloc[i, 1] == skempi1.iloc[j, 3]:
                skempi1.iloc[j, 19:48] = skempi2.iloc[i, :]

    skempi1.to_csv('combined.csv')


    print('yes')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
