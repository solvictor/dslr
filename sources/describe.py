from argparse import ArgumentParser
import pandas as pd


DDOF = 1


def mean(data):
    n = count(data)
    return sum(e for e in data if not pd.isna(e)) / n


def var(data):
    m = mean(data)
    n = count(data) - DDOF
    return sum((d - m) ** 2 for d in data if not pd.isna(d)) / n


def std(data):
    return var(data) ** 0.5


def ptp(data):
    return max(data) - min(data)


def percentile(percent):
    def inside(data):
        data_sorted = sorted(e for e in data if not pd.isna(e))
        rank = (len(data_sorted) - 1) * percent / 100
        lower_index = int(rank)
        upper_index = lower_index + 1
        lower_value = data_sorted[lower_index]
        upper_value = data_sorted[upper_index] if upper_index < len(data_sorted) else lower_value
        quantile_value = lower_value + (upper_value - lower_value) * (rank - lower_index)

        return quantile_value

    return inside


def count(data):
    return sum(not pd.isna(e) for e in data)


FUNCTIONS = {
    "Count": count,
    "Mean": mean,
    "Std": std,
    "Min": min,
    "25%": percentile(25),
    "50%": percentile(50),
    "75%": percentile(75),
    "Max": max,
    "Var": var,
    "PtP": ptp,
}


def parse_args():
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

    return parser.parse_args()


def main():
    args = parse_args()

    try:
        data = pd.read_csv(args.path)

        features = data.select_dtypes(include="number")
        # del features["Index"]
        features_data = {}
        for feature in features:
            feature_data = {}
            for name, fun in FUNCTIONS.items():
                feature_data[name] = fun(data[feature])
            features_data[feature] = feature_data

        SPACING = 8
        SPACES = " " * SPACING
        formatted = SPACES * 2 + SPACES.join(features) + "\n"
        for name in FUNCTIONS:
            formatted += (
                "{:<{}}".format(name, SPACING)
                + "".join(
                    "{:>{}.6f}".format(feature_data[name], SPACING + len(feature))
                    for feature, feature_data in features_data.items()
                )
                + "\n"
            )
        print(end=formatted)

    except FileNotFoundError:
        print(f"Error: File '{args.path}' not found.")
    except Exception as ex:
        print(f"Unexpected error occured : {ex}")


if __name__ == "__main__":
    main()
