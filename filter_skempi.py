import pandas as pd
import getopt
import math
import sys
import argparse


def parseArg():
    # parse output to take two inputs -i
    parser = argparse.ArgumentParser(
        description='Identify all points between two proteins that are within a certain distance of each other.')
    parser.add_argument('-i', nargs='?', metavar='Input_Skempi',
                        help='Input SKEMPI file to be filtered.')
    # parser.add_argument('-d', nargs='?', metavar='distance',
    #                     type=int, help='Resolution for distance checking.')
    # parser.add_argument('-o', nargs='?', metavar='OutputPDB',
    #                     help='Output PDB file name')

    # parse list of points from inputs
    args = parser.parse_args()
    args = vars(args)
    i = args['i']
    if i == None:
        i = 'combined_test.csv'
    return i


def charge_filter(combined, start_charge, end_charge):
    combined_filtered = pd.DataFrame().reindex_like(combined)
    mutation = combined['MutantList']

    for i in range(len(mutation)):
        c1 = 0
        c2 = 0

        multi_mutations = mutation.iloc[i].split(",")
        # print(multi_mutations)
        for m in multi_mutations:
            first = m[0]
            last = m[-1]
            if first == 'R' or first == 'H' or first == 'K':
                c1 = 1
            if first == 'D' or first == 'E':
                c1 = -1
            if last == 'R' or last == 'H' or last == 'K':
                c2 = 1
            if last == 'D' or last == 'E':
                c2 = -1
            if c1 == start_charge and c2 == end_charge:
                combined_filtered.iloc[i] = combined.iloc[i]

    print(combined_filtered)
    return combined_filtered


def main():
    i = parseArg()
    combined = pd.read_csv(i, index_col=0)
    charge_filter(combined, 0, 0)


if __name__ == "__main__":
    main()
