from argparse import ArgumentParser
import pandas as pd
from matplotlib import pyplot as plt


if __name__ == "__main__":
    parser = ArgumentParser(
        prog="scatter_plot",
        description="Create a scatter plot with a given csv dataset.",
    )

    parser.add_argument(
        "path",
        nargs="?",
        help="Path of the input csv dataset. Defaults to 'data/dataset_train.csv'.",
        default="data/dataset_train.csv",
    )

    args = parser.parse_args()

    try:
        data = pd.read_csv(args.path)

        data = data.dropna()  # delete rows containing NaNs
        features = data.iloc[:, 6:]  # Skip non-numerical features
        print(tuple(features))
        plt.scatter(features)
        plt.show()

    except Exception as ex:
        print(f"Failed to open '{args.path}': {ex.__class__.__name__} {ex}")
