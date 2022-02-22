import pandas as pd
import getopt
import math
import sys
import argparse


# parser function using argparse
# TODO: allow many different inputs for each type of filter to be done in order of inputs
def parseArg():
    # parse output to take inputs
    parser = argparse.ArgumentParser(
        description='Identify all points between two proteins that are within a certain distance of each other.')
    parser.add_argument('-i', nargs='?', metavar='Input_Skempi',
                        help='Input SKEMPI file to be filtered.')
    # parser.add_argument('-d', nargs='?', metavar='distance',
    #                     type=int, help='Resolution for distance checking.')
    # parser.add_argument('-o', nargs='?', metavar='OutputPDB',
    #                     help='Output PDB file name')

    # parse input file - if not given, set as default file i
    args = parser.parse_args()
    args = vars(args)
    i = args['i']
    if i == None:
        i = 'combined_test.csv'
    return i


# function to filter charges. Takes a dataframe input, and the desired start and end charges.
def charge_filter(combined, start_charge, end_charge):
    combined_filtered = pd.DataFrame().reindex_like(combined)
    mutation = combined['MutantList']

    # loop through mutant list column which contains all mutations
    for i in range(len(mutation)):
        # if multiple mutations exist, split by comma-separator and loop through each to check
        multi_mutations = mutation.iloc[i].split(",")
        # print(multi_mutations)
        for m in multi_mutations:
            c1 = 0
            c2 = 0
            # index [0] is first char in mutation list indicating 1st residue
            # index [-1] is last char in mutation list indicating 2nd residue
            first = m[0]
            last = m[-1]
            # check if residues are charged or not
            if first == 'R' or first == 'H' or first == 'K':
                c1 = 1
            if first == 'D' or first == 'E':
                c1 = -1
            if last == 'R' or last == 'H' or last == 'K':
                c2 = 1
            if last == 'D' or last == 'E':
                c2 = -1
            # if charge of residues are equal to desired charge, write to new dataframe
            if c1 == start_charge and c2 == end_charge:
                combined_filtered.iloc[i] = combined.iloc[i]

    combined_filtered.dropna(subset=["PDBCode"], inplace=True)

    print(combined_filtered)
    return combined_filtered


def main():
    i = parseArg()
    combined = pd.read_csv(i, index_col=0)
    charge_filter(combined, 0, 0)


if __name__ == "__main__":
    main()
