import pandas as pd


def main():
    combined = pd.read_csv('combined.csv', index_col=0)


if __name__ == "__main__":
    main()
