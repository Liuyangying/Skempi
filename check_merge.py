import pandas as pd


def main():
    combined = pd.read_csv('combined.csv', index_col=0)
    volumes_sheet = pd.read_excel(
        'Final Integrated Volumes (Skempi Dataset).xlsx', index_col=0)
    skempi = pd.read_excel('Copy of skempi_v2(1).xlsx')

    print("Checking file length...")
    print(len(combined) == len(volumes_sheet))

    print("Checking same number of each PDB entry")
    df = pd.DataFrame(
        {'a': combined.iloc[:, 0], 'b': volumes_sheet.iloc[:, 0]})
    check1 = df.groupby(['a']).size()
    check2 = df.groupby(['b']).size()
    print(check1[0])
    # for i in len(check1):
    #     if check1[i] != check2[i]:
    #         print(check1[i])


if __name__ == "__main__":
    main()
