import pandas as pd
import numpy as np
from process_skempi import average_elec_sheet


def remove_multi(sheet):

    """
    remove multiple mutations records, only keep single mutation records
    """
    mvmulti_sheet = sheet
    mvmulti_sheet['MutantList'] = mvmulti_sheet['MutantList'].apply(lambda x: 0 if len(x.split(',')) > 1 else x)

    drop = mvmulti_sheet['MutantList'][mvmulti_sheet['MutantList']==0]
    mvmulti_sheet = mvmulti_sheet.drop(drop.index)

    return mvmulti_sheet


def elect_s4169(path1, path2):

    sgl_sheet = average_elec_sheet(path1)
    s4169 = pd.read_csv(path2)
    s4169.insert(0, "PDB_mut", s4169['pdb'] + '_' + s4169['mutation'])
    s4169_act = s4169.drop(['pdb', 'mutation', 'mcsm_ppi2_prediction', 'sampling_fold'], axis=1)
    s4169_act = s4169_act.drop_duplicates(subset=['PDB_mut'])
    filter_sheet = pd.merge(sgl_sheet, s4169_act, on='PDB_mut', how='inner')

    return filter_sheet


def elect_s378(path1, path2):

    sgl_sheet = average_elec_sheet(path1)
    s378 = pd.read_csv(path2)
    s378['mutation'] = s378['mutation'].str[0] + s378['chain'] + s378['mutation'].str[1:]
    s378.insert(0, "PDB_mut", s378['pdb'] + '_' + s378['mutation'])
    s378_act = s378.drop(['pdb', 'mutation', 'mcsm_ppi2_prediction'], axis=1)
    s378_act = s378_act.drop_duplicates(subset=['PDB_mut'])
    filter_sheet = pd.merge(sgl_sheet, s378_act, on='PDB_mut', how='inner')

    return filter_sheet


def skempi_process(path):

    skempi = pd.read_csv(
        'D:\PycharmProjects\Skempiv2\compare dataset with benchmark dataset\skempi_v2.csv', header=None)
    skempi = skempi.dropna(axis=1, how='all')

    # temp = skempi.apply(lambda x: x.apply(lambda c: [str(c)] if type(c) == float else c.split(";")))
    temp = skempi
    # test = test.apply(lambda x: x.str.cat(sep=';', na_rep=' '))
    temp2 = temp[0]
    for i in range(1, len(temp.columns)):
        temp2 = temp2.str.cat(temp[i], sep=';', na_rep=' ')
    temp2.to_csv('skempi2_processed.csv', index=False)




if __name__ == '__main__':

    path1 = 'D:\PycharmProjects\Skempiv2\compare dataset with benchmark dataset\Final Integrated Volumes (Skempi Dataset).csv'
    path2 = 'D:\PycharmProjects\Skempiv2\compare dataset with benchmark dataset\s4169.csv'
    path3 = 'D:\PycharmProjects\Skempiv2\compare dataset with benchmark dataset\s378.csv'
    elect_s4169_sheet = elect_s4169(path1, path2)
    elect_s378_sheet = elect_s378(path1, path3)

    elect_s4169_sheet.to_csv('elect_s4169_sheet.csv')
    elect_s378_sheet.to_csv('elect_s378_sheet.csv')

    path = 'D:\PycharmProjects\Skempiv2\compare dataset with benchmark dataset\skempi_v2.csv'
    skempi_process(path)

    skempi_sep = pd.read_csv(
        'D:\\PycharmProjects\\Skempiv2\\compare dataset with benchmark dataset\\skempi2_processed_sep.csv')
    location = ['COR', 'INT', 'SUP', 'RIM', 'SUR']
    COR = skempi_sep[skempi_sep['iMutation_Location(s)'] == 'COR']
    INT = skempi_sep[skempi_sep['iMutation_Location(s)'] == 'INT']
    SUP = skempi_sep[skempi_sep['iMutation_Location(s)'] == 'SUP']
    RIM = skempi_sep[skempi_sep['iMutation_Location(s)'] == 'RIM']
    SUR = skempi_sep[skempi_sep['iMutation_Location(s)'] == 'SUR']
    SKEMPI_single = [COR, INT, SUP, RIM, SUR]
    SKEMPI_single = pd.concat(SKEMPI_single)
    SKEMPI_single.to_csv('skempi2_processed_3.csv', index=False)


    # final_sheet = pd.DataFrame(0, index=np.arange(7085), columns=test[0])
    # sgl_sheet = remove_multi(concate_sheet)
    # sgl_sheet.insert(1, "PDB_mut",  sgl_sheet['PDBCode']+'_'+sgl_sheet['MutantList'])
    # s4169.insert(0, "PDB_mut", s4169['pdb'] + '_' + s4169['mutation'])
    # s4169_act = s4169.drop(['pdb','mutation','mcsm_ppi2_prediction','sampling_fold'],axis=1)
    # filter_sheet = pd.merge(sgl_sheet,s4169_act, on='PDB_mut', how = 'inner')
    # test = filter_sheet[filter_sheet['PDB_mut'].duplicated(keep=False)]
    # test2 = s4169_act['PDB_mut'].duplicated(keep=False)



    print("yes")
