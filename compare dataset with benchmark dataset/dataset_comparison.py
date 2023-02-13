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


    s378 = pd.read_csv('F:\PycharmProjects\\407 Project\\407 project\compare dataset with benchmark dataset\s378.csv')
    # print(len(s378))

    s4169 = pd.read_csv('F:\PycharmProjects\\407 Project\\407 project\compare dataset with benchmark dataset\s4169.csv')
    # print(len(s4169))

    skempi = pd.read_csv(
        'F:\PycharmProjects\\407 Project\\407 project\compare dataset with benchmark dataset\skempi_v2.csv', header=None)
    skempi = skempi.dropna(axis=1, how='all')

    test = skempi.apply(lambda x: x.apply(lambda c: [str(c)] if type(c)==float else c.split(";")))
    test2 = test[0]
    for i in range(len(test.columns)):
            test2 = test2 +test[i]


    final_sheet = pd.DataFrame(0, index=np.arange(7085), columns=test[0])

    test3= test2.apply(lambda x: len(x))

    sgl_sheet = remove_multi(concate_sheet)


    sgl_sheet.insert(1, "PDB_mut",  sgl_sheet['PDBCode']+'_'+sgl_sheet['MutantList'])
    s4169.insert(0, "PDB_mut", s4169['pdb'] + '_' + s4169['mutation'])
    s4169_act = s4169.drop(['pdb','mutation','mcsm_ppi2_prediction','sampling_fold'],axis=1)
    filter_sheet = pd.merge(sgl_sheet,s4169_act, on='PDB_mut', how = 'inner')

    test = filter_sheet[filter_sheet['PDB_mut'].duplicated(keep=False)]
    test2 = s4169_act['PDB_mut'].duplicated(keep=False)


    print("yes")
