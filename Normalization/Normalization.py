import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

def find_min_max(sheet):

     mut_1_1_max = sheet['[MUTA]ELEC_-1+1'].max()
     mut_1_1_min = sheet['[MUTA]ELEC_-1+1'].min()
     ori_1_1_max = sheet['[ORIG]ELEC_-1+1'].max()
     ori_1_1_min = sheet['[ORIG]ELEC_-1+1'].min()

     max_1_1 = max(mut_1_1_max, ori_1_1_max)
     min_1_1 = min(mut_1_1_min, ori_1_1_min)

     mut_1_2_max = sheet['[MUTA]ELEC_+1-1'].max()
     mut_1_2_min = sheet['[MUTA]ELEC_+1-1'].min()
     ori_1_2_max = sheet['[ORIG]ELEC_+1-1'].max()
     ori_1_2_min = sheet['[ORIG]ELEC_+1-1'].min()

     max_1_2 = max(mut_1_2_max, ori_1_2_max)
     min_1_2 = min(mut_1_2_min,ori_1_2_min)

     mut_5_1_max = sheet['[MUTA]ELEC_-5+5'].max()
     mut_5_1_min = sheet['[MUTA]ELEC_-5+5'].min()
     ori_5_1_max = sheet['[ORIG]ELEC_-5+5'].max()
     ori_5_1_min = sheet['[ORIG]ELEC_-5+5'].min()

     max_5_1 = max(mut_5_1_max, ori_5_1_max)
     min_5_1 = min(mut_5_1_min, ori_5_1_min)

     mut_5_2_max = sheet['[MUTA]ELEC_+5-5'].max()
     mut_5_2_min = sheet['[MUTA]ELEC_+5-5'].min()
     ori_5_2_max = sheet['[ORIG]ELEC_+5-5'].max()
     ori_5_2_min = sheet['[ORIG]ELEC_+5-5'].min()

     max_5_2 = max(mut_5_2_max, ori_5_2_max)
     min_5_2 = min(mut_5_2_min, ori_5_2_min)

     mut_intersect_max = sheet['[MUTA]MS_INTERSECT'].max()
     mut_intersect_min = sheet['[MUTA]MS_INTERSECT'].min()
     ori_intersect_max = sheet['[ORIG]MS_INTERSECT'].max()
     ori_intersect_min = sheet['[ORIG]MS_INTERSECT'].min()
     max_intersect = max(mut_intersect_max,ori_intersect_max)
     min_intersect = min(mut_intersect_min,ori_intersect_min)

     return max_1_1,min_1_1,max_1_2,min_1_2,max_5_1,min_5_1,max_5_2,min_5_2,max_intersect,min_intersect


if __name__ == '__main__':

     path = 'F:\\PycharmProjects\\combine_sheet\\Normalization\\All_features_3.csv'

     sheet = pd.read_csv(path)

     sheet = sheet[sheet['Orig_G']!='#NUM!']
     sheet = sheet[sheet['[DIFF]ELEC_+5-5']!=' ' ]
     sheet['[DIFF]ELEC_+5-5'] = sheet['[DIFF]ELEC_+5-5'].astype('float')
     #sheet['[DIFF]ELEC_+5-5']  = pd.to_numeric(sheet['[DIFF]ELEC_+5-5'] , errors='coerce')
     sheet['Orig_G'] = sheet['Orig_G'].astype('float')
     sheet['Diff_G'] = sheet['Diff_G'].astype('float')
     columns = sheet.columns

     max_1_1, min_1_1, max_1_2, min_1_2, max_5_1, min_5_1, max_5_2, min_5_2,max_intersect,min_intersect= find_min_max(sheet)

     sheet['[MUTA]ELEC_-1+1'] = (sheet['[MUTA]ELEC_-1+1']-min_1_1)/(max_1_1-min_1_1)
     sheet['[ORIG]ELEC_-1+1'] = (sheet['[ORIG]ELEC_-1+1'] - min_1_1) / (max_1_1 - min_1_1)
     sheet['[DIFF]ELEC_-1+1'] = (sheet['[DIFF]ELEC_-1+1']- min_1_1) / (max_1_1 - min_1_1)

     sheet['[MUTA]ELEC_+1-1'] = (sheet['[MUTA]ELEC_+1-1'] - min_1_2) / (max_1_2 - min_1_2)
     sheet['[ORIG]ELEC_+1-1'] = (sheet['[ORIG]ELEC_+1-1'] - min_1_2) / (max_1_2 - min_1_2)
     sheet['[DIFF]ELEC_+1-1'] = (sheet['[DIFF]ELEC_+1-1']- min_1_2) / (max_1_2 - min_1_2)

     sheet['[MUTA]ELEC_-5+5'] = (sheet['[MUTA]ELEC_-5+5'] - min_5_1)/ (max_5_1-min_5_1)
     sheet['[ORIG]ELEC_-5+5'] = (sheet['[ORIG]ELEC_-5+5'] - min_5_1)/ (max_5_1-min_5_1)
     sheet['[DIFF]ELEC_-5+5'] = (sheet['[DIFF]ELEC_-5+5']- min_5_1) / (max_5_1 - min_5_1)

     sheet['[MUTA]ELEC_+5-5'] = (sheet['[MUTA]ELEC_+5-5'] - min_5_2) / (max_5_2 - min_5_2)
     sheet['[ORIG]ELEC_+5-5'] = (sheet['[ORIG]ELEC_+5-5'] - min_5_2) / (max_5_2 - min_5_2)
     sheet['[DIFF]ELEC_+5-5'] = (sheet['[DIFF]ELEC_+5-5']- min_5_2) / (max_5_2 - min_5_2)

     sheet['[MUTA]MS_INTERSECT'] = (sheet['[MUTA]MS_INTERSECT']-min_intersect)/(max_intersect-min_intersect)
     sheet['[ORIG]MS_INTERSECT'] = (sheet['[ORIG]MS_INTERSECT']-min_intersect)/(max_intersect-min_intersect)
     sheet['[DIFF]MS_INTERSECT'] = (sheet['[DIFF]MS_INTERSECT']-min_intersect)/(max_intersect-min_intersect)

     sheet['Distance_to_interface']=(sheet['Distance_to_interface']-sheet['Distance_to_interface'].min())/(sheet['Distance_to_interface'].max()-sheet['Distance_to_interface'].min())

     Ori_hydrophobicity_min = sheet['Orig_hydrophobicity'].min()
     Ori_hydrophobicity_max = sheet['Orig_hydrophobicity'].max()
     mut_hydrophobicity_min = sheet['Mut_hydrophobicity'].min()
     mut_hydrophobicity_max = sheet['Mut_hydrophobicity'].max()

     hydrophobicity_min = min(Ori_hydrophobicity_min,mut_hydrophobicity_min)
     hydrophobicity_max = max(Ori_hydrophobicity_max,mut_hydrophobicity_max)
     sheet['Orig_hydrophobicity'] = (sheet['Orig_hydrophobicity']-hydrophobicity_min)/(hydrophobicity_max-hydrophobicity_min)
     sheet['Mut_hydrophobicity'] = (sheet['Mut_hydrophobicity']-hydrophobicity_min)/(hydrophobicity_max-hydrophobicity_min)

     Ori_size_min = sheet['Orig_size'].min()
     Ori_size_max = sheet['Orig_size'].max()
     mut_size_min = sheet['Mut_size'].min()
     mut_size_max = sheet['Mut_size'].max()

     size_min = min(Ori_size_min, mut_size_min)
     size_max = max(Ori_size_max, mut_size_max)
     sheet['Orig_size'] = (sheet['Orig_size'] - size_min) / (
                  size_max -size_min)
     sheet['Mut_size'] = (sheet['Mut_size'] - size_min) / (
                  size_max - size_min)


     sheet.to_csv('all_features_normalized.csv')

     print('yes')