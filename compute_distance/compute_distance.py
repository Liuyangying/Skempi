import numpy

import pandas as pd
import numpy as np
from Bio.PDB.PDBParser import PDBParser
import os
import re

def load_pdb(filename):

    '''
    load pdb file as dataframe
    :param filename:
    :return:
    '''

    path = "F:\PycharmProjects\combine_sheet\\compute_distance\\filtered_PDB\\" + filename
    structure = []
    with open(path) as pdb_file:

        lines = pdb_file.readlines()

        for line in lines:
            temp = line.split()
            #atomtype and amino acid link together
            if len(temp[2])>4:
                comb = temp.pop(2)
                atom,ami_ac = comb[0:3],comb[3:]
                temp.insert(2,atom)
                temp.insert(3,ami_ac)
            #chain name and amino acid name link together
            if len(temp[4])>1:
                chain_num = temp.pop(4)
                chain = chain_num[0]
                a_num = chain_num[1:]
                temp.insert(4,chain)
                temp.insert(5,a_num)

            #x axis value and y axis value link together
            if len(temp[6].split('-')) == 2 and '' not in temp[6].split('-'):
                xy = temp.pop(6)
                x = xy.split('-')[0]
                y = '-'+ xy.split('-')[1]
                temp.insert(6, x)
                temp.insert(7, y)
            elif len(temp[6].split('-')) == 3 and '' in temp[6].split('-'):
                xy = temp.pop(6)
                x = '-'+ xy.split('-')[1]
                y = '-'+ xy.split('-')[2]
                temp.insert(6, x)
                temp.insert(7, y)
            elif len(temp[6].split('-')) == 4 and '' in temp[6].split('-'):
                xyz = temp.pop(6)
                x = '-'+ xyz.split('-')[1]
                y = '-'+ xyz.split('-')[2]
                z = '-'+ xyz.split('-')[3]
                temp.insert(6, x)
                temp.insert(7, y)
                temp.insert(8, z)


            #y axis value and z axis value link together
            if len(temp[7].split('-'))==2 and '' not in temp[7].split('-') :
                yz = temp.pop(7)
                y = yz.split('-')[0]
                z = '-'+ yz.split('-')[1]
                temp.insert(7, y)
                temp.insert(8, z)
            elif len(temp[7].split('-'))==3 and '' in temp[7].split('-'):
                yz = temp.pop(7)
                y = '-' + yz.split('-')[1]
                z = '-' + yz.split('-')[2]
                temp.insert(7, y)
                temp.insert(8, z)

            #occupation and temperature link together
            if len(temp) != 12:
                try:
                    temp.append(temp[10])
                    temp[9], temp[10] = temp[9][0:4], temp[9][4:]
                except:
                    print(filename,temp)

            structure.append(temp)
            s = pd.DataFrame(structure)

    name = filename.split('.')[0]

    return s, name


def check_residue(s,name):

    '''check if numbers of residues are consecutive and if the amino acid number include insertion code'''

    chain = s[4].unique()
    incontinuity = []
    insertion = []
    for i in range(0,len(chain)):
        #s[4] is chain name, s[5] is number of residue on chain
        half_num = s[s[4]== chain[i]][5]
        for n in half_num.index:
            try:
                if half_num[n][-1].isalpha():
                    insertion.append([name, chain[i], half_num[n]])
                    half_num[n] = half_num[n].strip(half_num[n][-1])

            except:
                print(half_num.shape, half_num[n])
        try:
            #half_num = half_num.unique().astype(int)
            half_num = half_num.astype(int)

        except:
            print(name,half_num)
        #half_num = s[s[4]== chain[i]][5].unique().astype(int)

        half_diff = np.diff(half_num)

        #index = np.argwhere(half_diff>1)+1
        index = np.argwhere(half_diff > 1)+1

        #try:
        if len(index) != 0:
            print(index)
            amino_num = [half_num.iloc[i[0]] for i in index]
            print(amino_num)
            incontinuity.append([name, chain[i],amino_num])

        #print([name, chain[i], amino_num])

    insertion = np.array(insertion)

    return incontinuity, insertion

def distance_cal(mutation,half1,half2,s):

    #mutation = 'DB60aA'
    # half1 = 'I'
    # half2 = 'E'
    # half1 = 'B'
    # half2 = 'CD'
    mutation = str.upper(mutation)
    #wild_ami = mutation[0]
    #mut_ami = mutation[-1]
    #Position include chain and amino acid number
    position = mutation[1:-1]

    #mut_ami keep the chain which include the mutated amino acid
    mut_ami = s[s[4] == position[0]]
    #mut_ami_atom keep the mutated amino acid information
    mut_ami_atom = mut_ami[mut_ami[5] == position[1:]]
    #keep the x y z valuse of the mutated amino acid and transfer it into numpy array
    mut_ami_atom = np.array(mut_ami_atom.iloc[:, 6:9])

    if position[0] in half1:
        half = half1
    elif position[0] in half2:
        half = half2

    for i in range(0, len(half)):
        list = s[s[4] == half[i]].index
        s = s.drop(list)
        another_half = np.array(s.iloc[:, 6:9])

    #print(len(mut_ami_atom), len(another_half))
    distance = np.zeros((len(mut_ami_atom), len(another_half)))
    mut_ami_atom = mut_ami_atom.astype(float)
    another_half = another_half.astype(float)

    for j in range(0, len(mut_ami_atom)):
        dist_vec = np.sqrt(np.sum(np.square(another_half - mut_ami_atom[j]), axis=1))
        distance[j] = dist_vec

    dist = distance.min()

    return dist


def add_distance_to_sheet(cleaned_sheet):

    cleaned_sheet['Ori_dist'] = 0

    for i in range(0,len(cleaned_sheet)):
        pdb = '{}.pdb'.format(cleaned_sheet.iloc[i, 1])
        half1 = cleaned_sheet.iloc[i, 2]
        half2 = cleaned_sheet.iloc[i, 3]
        mutation = cleaned_sheet.iloc[i, 4]
        s,name = load_pdb(pdb)
        #np.save('{}.npy'.format(name),s)
        dist = distance_cal(mutation, half1, half2, s)
        cleaned_sheet.iloc[i,-1] = dist

    return cleaned_sheet



if __name__ == '__main__':

    cleaned_sheet = pd.read_csv('F:\PycharmProjects\combine_sheet\\compute_distance\clean_sheet_temp_affi.csv', index_col=0)
    for i in range(0,len(cleaned_sheet)):
        if '1.00E' in cleaned_sheet.iloc[i,1]:
            cleaned_sheet.iloc[i, 1] = cleaned_sheet.iloc[i,0].split('_')[0]
    # pdb = '{}.pdb'.format(cleaned_sheet.iloc[0, 1])
    # print(pdb)
    # add_distance_to_sheet(cleaned_sheet)
    # structure_id = "1CSE"
    # filename = "F:\PycharmProjects\combine_sheet\\compute_distance\\filtered_PDB\\1ACB.pdb"
    # s = p.get_structure(structure_id, filename)

    #filename = "F:\PycharmProjects\combine_sheet\\compute_distance\\filtered_PDB\\1ACB.pdb"
    #filename = "F:\PycharmProjects\combine_sheet\\compute_distance\\filtered_PDB\\1CSE.pdb"
    #filename = '4GXU.pdb'
    #filename = '3U82.pdb'
    #filename = '4FZA.pdb'
    #filename = '4X4M.pdb'
    #filename = '1CSE.pdb'
    filename = '4OZG.pdb'
    s, namepdb=load_pdb(filename)
    # incontinuity,insertion = check_residue(s,namepdb)
    mutation = 'NG36A'
    half1 = 'ABJ'
    half2 = 'GH'
    dist = distance_cal(mutation, half1, half2,s)

    #
    # path = "F:\PycharmProjects\combine_sheet\\compute_distance\\filtered_PDB"
    # files_list = os.listdir(path)

    # incontinuity_all = []
    # for pdb in files_list:
    #     s,name = load_pdb(pdb)
    #     incontinuity = check_residue(s,name)
    #     incontinuity_all = incontinuity_all + incontinuity

    print("yes")