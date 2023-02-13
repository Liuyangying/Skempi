import pandas as pd
import numpy as np

def remove_multi(sheet):

    """
    remove multiple mutations records, only keep single mutation records
    """
    mvmulti_sheet = sheet
    mvmulti_sheet['MutantList'] = mvmulti_sheet['MutantList'].apply(lambda x: 0 if len(x.split(',')) > 1 else x)

    drop = mvmulti_sheet['MutantList'][mvmulti_sheet['MutantList']==0]
    mvmulti_sheet = mvmulti_sheet.drop(drop.index)

    return mvmulti_sheet


if __name__ == '__main__':


    concate_sheet =pd.read_csv('F:\PycharmProjects\\407 Project\\407 project\compare dataset with benchmark dataset\Concate.csv')
    print(len(concate_sheet))
    colnames = concate_sheet.columns
    concate_sheet = concate_sheet.drop(['WorkIndex', '#Pdb',
       'Mutation(s)_PDB', 'Mutation(s)_cleaned', 'iMutation_Location(s)',
       'Hold_out_type', 'Hold_out_proteins', 'Affinity_mut (M)',
       'Affinity_mut_parsed', 'Affinity_wt (M)', 'Affinity_wt_parsed',
       'Reference', 'Protein 1', 'Protein 2', 'Temperature',
       'kon_mut (M^(-1)s^(-1))', 'kon_mut_parsed', 'kon_wt (M^(-1)s^(-1))',
       'kon_wt_parsed', 'koff_mut (s^(-1))', 'koff_mut_parsed',
       'koff_wt (s^(-1))', 'koff_wt_parsed', 'dH_mut (kcal mol^(-1))',
       'dH_wt (kcal mol^(-1))', 'dS_mut (cal mol^(-1) K^(-1))',
       'dS_wt (cal mol^(-1) K^(-1))', 'Notes', 'Method',
       'SKEMPI version,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,'],axis=1)

    s378 = pd.read_csv('F:\PycharmProjects\\407 Project\\407 project\compare dataset with benchmark dataset\s378.csv')
    # print(len(s378))

    s4169 = pd.read_csv('F:\PycharmProjects\\407 Project\\407 project\compare dataset with benchmark dataset\s4169.csv')
    # print(len(s4169))
    s4169.insert(0, "PDB_mut",  s4169['pdb']+'_'+s4169['mutation'])
    sgl_sheet = remove_multi(concate_sheet)
    sgl_sheet.insert(1, "PDB_mut", sgl_sheet['PDBCode'] + '_' + sgl_sheet['MutantList'])
    # filter_sheet = pd.merge(s4169,sgl_sheet, on='PDB_mut', how='right')
    # filter_sheet = sgl_sheet.drop_duplicates(subset=['PDB_mut'])
    s4169 = s4169.drop_duplicates(subset=['PDB_mut'])
    mergesheet = pd.concat(s4169, sgl_sheet, on='PDB_mut', how='left')
    # skempi = pd.read_csv(
    #     'F:\PycharmProjects\\407 Project\\407 project\compare dataset with benchmark dataset\skempi_v2.csv', header=None)
    # skempi = skempi.dropna(axis=1, how='all')
    #
    # test = skempi.apply(lambda x: x.apply(lambda c: [str(c)] if type(c)==float else c.split(";")))
    # test2 = test[0]
    # for i in range(len(test.columns)):
    #         test2 = test2 +test[i]
    #
    #
    # final_sheet = pd.DataFrame(0, index=np.arange(7085), columns=test[0])
    #
    # test3= test2.apply(lambda x: len(x))
    #
    # sgl_sheet = remove_multi(concate_sheet)
    #
    #
    # sgl_sheet.insert(1, "PDB_mut",  sgl_sheet['PDBCode']+'_'+sgl_sheet['MutantList'])
    # s4169.insert(0, "PDB_mut", s4169['pdb'] + '_' + s4169['mutation'])
    # s4169_act = s4169.drop(['pdb','mutation','mcsm_ppi2_prediction','sampling_fold'],axis=1)
    # filter_sheet = pd.merge(sgl_sheet,s4169_act, on='PDB_mut', how = 'inner')
    #
    # test = filter_sheet[filter_sheet['PDB_mut'].duplicated(keep=False)]
    # test2 = s4169_act['PDB_mut'].duplicated(keep=False)


    print("yes")
