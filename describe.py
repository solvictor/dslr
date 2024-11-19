#!/bin/python3

from argparse import ArgumentParser
import pandas as pd


def mean(data):
    return sum(data) / len(data)


def std(data):
    m = mean(data)
    return (sum((d - m) ** 2 for d in data) / len(data)) ** 0.5


def percentile(percent):
    def inside(data):
        data_sorted = sorted(data)
        rank = (len(data) - 1) * percent / 100
        lower_index = int(rank)
        upper_index = lower_index + 1
        lower_value = data_sorted[lower_index]
        upper_value = data_sorted[upper_index] if upper_index < len(data) else lower_value
        quantile_value = lower_value + (upper_value - lower_value) * (rank - lower_index)

        return quantile_value

    return inside


FUNCTIONS = {
    "Count": len,
    "Mean": mean,
    "Std": std,
    "Min": min,
    "25%": percentile(25),
    "50%": percentile(50),
    "75%": percentile(75),
    "Max": max,
}

if __name__ == "__main__":
    parser = ArgumentParser(
        prog="describe",
        description="Create a description of a given csv dataset.",
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

        features_data = {}
        for feature in features:
            feature_data = {}
            for name, fun in FUNCTIONS.items():
                feature_data[name] = fun(data[feature])
            features_data[feature] = feature_data
        print(" " * 8, *features, sep=" " * 8)
        for name in FUNCTIONS:
            print(
                f"{name:<8}"
                + "".join(
                    "{:>{}.6f}".format(feature_data[name], 8 + len(feature))
                    for feature, feature_data in features_data.items()
                )
            )
    except Exception as ex:
        print(f"Failed to open '{args.path}': {ex.__class__.__name__} {ex}")
