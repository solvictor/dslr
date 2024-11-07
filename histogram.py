from argparse import ArgumentParser
import pandas as pd

if __name__ == "__main__":
    parser = ArgumentParser(
        prog="histogram",
        description="Plot histograms of Hogwarts course scores for each house.",
    )

    parser.add_argument(
        "--path",
        type=str,
        default="data/dataset_test.csv",
        help=(
            "Path to the input CSV dataset."
            "Defaults to 'data/dataset_test.csv' if not specified."
        ),
    )

    args = parser.parse_args()

    try:
        data = pd.read_csv(args.path)
    except FileNotFoundError:
        print(f"Error: File '{args.path}' not found.")
    except Exception as ex:
        print(f"Unexpected error occured : {ex}")
