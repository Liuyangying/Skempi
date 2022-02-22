import pandas as pd

# The combined sheet is matched with Brian's calculation sheet rather than SKEMPI dataset.
# This means any missing structures in volumes_sheet are reflected in combined sheet.


def main():
    # read files for checking

    combined = pd.read_csv('combined.csv', index_col=0)
    volumes_sheet = pd.read_excel(
        'Final Integrated Volumes (Skempi Dataset).xlsx', index_col=0)
    skempi = pd.read_excel('Copy of skempi_v2(1).xlsx')

    # checking file length by number of lines.
    print("Checking file length...")
    print(len(combined) == len(volumes_sheet))

    # checking number of PDB entries to make sure each unique entry shows up the same number of times.
    # Create a dataframe containing column with all PDB names, group by unique name, count, and compare counts.
    print("Checking same number of each PDB entry...")
    df = pd.DataFrame(
        {'a': combined.iloc[:, 0], 'b': volumes_sheet.iloc[:, 0]})
    check1 = df.groupby(['a']).size()
    check2 = df.groupby(['b']).size()
    print(check1 == check2)
    # for i in len(check1):
    #     if check1[i] != check2[i]:
    #         print(check1[i])

    print("Checking same number of mutants...")


if __name__ == "__main__":
    main()
