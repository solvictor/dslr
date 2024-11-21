from argparse import ArgumentParser
from matplotlib import pyplot as plt
from pandas.api.types import is_float_dtype
import pandas as pd
import seaborn as sns


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
        df = data.dropna()

        for first_idx, first_course in enumerate(df):
            if not is_float_dtype(df[first_course]):
                continue
            for _, second_course in enumerate(df, first_idx + 1):
                if not is_float_dtype(df[second_course]):
                    continue

                plt.figure("Scatter plot", figsize=(10, 6))
                sns.scatterplot(
                    data=df,
                    x=first_course,
                    y=second_course,
                    hue="Hogwarts House",
                )

                plt.title(
                    f"Scatter plot of {first_course} against {second_course} Scores by Hogwarts House"
                )
                plt.xlabel("Score")
                plt.ylabel("Frequency")

                plt.show()

    except Exception as ex:
        print(f"Failed to open '{args.path}': {ex.__class__.__name__} {ex}")
