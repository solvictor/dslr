from argparse import ArgumentParser
import pandas as pd


if __name__ == "__main__":
    parser = ArgumentParser(
        prog="describe",
        description="Create a description of a given csv dataset.",
    )

    parser.add_argument("path", type=str, help="Path of the input csv dataset.")

    args = parser.parse_args()

    try:
        data = pd.read_csv(args.path)
        for j in data:
            print(j)
    except Exception as ex:
        print(f"Failed to open '{args.path}': {ex}")
