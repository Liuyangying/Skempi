import pandas as pd
import numpy as np


def average_affinity_skempi(path):

    "average affinity of same PDB and mutation records"

    skempi = pd.read_csv(path)
    skempi.insert(0, "PDB_mut", skempi['#Pdb'] + '_' + skempi['Mutation(s)_PDB'])
    skempi2 = skempi.drop(['#Pdb','Mutation(s)_PDB','Mutation(s)_cleaned','iMutation_Location(s)','Affinity_mut (M)','Affinity_wt (M)',' ','SKEMPI version'],axis=1)

    skempi_nondup = skempi2.iloc[:,0:3]
    skempi_nondup = skempi_nondup.groupby('PDB_mut').mean()

    skempi_nondup['Affinity_mut_parsed'] = skempi_nondup['Affinity_mut_parsed'].apply(lambda x: "{:.2e}".format(x))
    skempi_nondup['Affinity_wt_parsed'] = skempi_nondup['Affinity_wt_parsed'].apply(lambda x: "{:.2e}".format(x))

    skempi2['Affinity_mut_parsed'] = skempi2['Affinity_mut_parsed'].apply(lambda x: "{:.2e}".format(x))
    skempi2['Affinity_wt_parsed'] = skempi2['Affinity_wt_parsed'].apply(lambda x: "{:.2e}".format(x))

    # skempi_nondup['PDB_mut'] = skempi_nondup.index
    skempi_nondup.insert(0, "PDB_mut", skempi_nondup.index)
    skempi_nondup.index = range(len(skempi_nondup))
    temp = skempi.loc[:,['iMutation_Location(s)','PDB_mut']]
    temp = temp.drop_duplicates(subset=['PDB_mut'])
    # temp['PDB_mut'] = temp['PDB_mut'].apply(lambda x: x.split('_')[0]+"_"+x.split('_')[-1])
    skempi_nondup = pd.merge(skempi_nondup,temp, on='PDB_mut', how = 'inner')

    return skempi_nondup


def average_elec_sheet(path):

    "average electrostatic potential of same PDB and mutation records"

    electr_sheet = pd.read_csv(path)
    # electr_sheet['PDBCode']
    # names = electr_sheet.columns
    electr_sheet.insert(0, "PDB_mut",  electr_sheet['PDBCode']+'_'+electr_sheet['MutantList'])
    electr_sheet2 = electr_sheet.drop(['WorkIndex', 'PDBCode', 'Chain1', 'Chain2', 'MutantList',
       'Unnamed: 20', 'Unnamed: 21', 'Unnamed: 22', 'Unnamed: 23',
       'Unnamed: 24', 'Unnamed: 25'],axis=1)
    electr_sheet3 = electr_sheet.loc[:,['PDBCode', 'Chain1', 'Chain2', 'MutantList']]
    electr_sheet3.insert(0, "PDB_mut", electr_sheet3['PDBCode']+'_'+electr_sheet3['MutantList'])
    electr_sheet3 = electr_sheet3.drop_duplicates(subset=['PDB_mut'])

    electr_sheet2 = electr_sheet2.groupby('PDB_mut').mean()
    electr_sheet2.insert(0, "PDB_mut", electr_sheet2.index)
    electr_sheet2.index = range(len(electr_sheet2))
    electr_sheet2['PDB_mut'] = electr_sheet2['PDB_mut'].apply(lambda x: 0 if len(x.split(','))>1 else x)
    electr_sheet2 = electr_sheet2[electr_sheet2['PDB_mut'] != 0]
    merge_electr_sheet = pd.merge(electr_sheet3, electr_sheet2, on='PDB_mut', how='inner')

    return merge_electr_sheet


if __name__ == '__main__':

    path = 'D:\PycharmProjects\Skempiv2\compare dataset with benchmark dataset\skempi2_processed_final(4958).csv'
    skempi_nondup = average_affinity_skempi(path)
    # print(skempi.iloc[0,1])

    skempi_nondup['PDB_mut'] = skempi_nondup['PDB_mut'].apply(lambda x:x.split('_')[0]+'_'+x.split('_')[-1])

    path2 = 'D:\PycharmProjects\Skempiv2\compare dataset with benchmark dataset\Final Integrated Volumes (Skempi Dataset).csv'
    electr_sheet_average = average_elec_sheet(path2)
    merge_sheet = pd.merge(skempi_nondup, electr_sheet_average, on='PDB_mut', how='inner')

    merge_sheet.to_csv("concat_norep_sheet(3618).csv")


    print('yes')