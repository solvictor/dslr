from argparse import ArgumentParser
from pandas.api.types import is_float_dtype
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


DEFAULT_LOCATION_HISTOGRAM_IMAGES = "histograms"
DEFAULT_LOCATION_FILE_DATASET = "data/dataset_train.csv"


if __name__ == "__main__":
    parser = ArgumentParser(
        prog="histogram",
        description="Plot histograms of Hogwarts course scores for each house.",
    )

    parser.add_argument(
        "--path",
        type=str,
        default=DEFAULT_LOCATION_FILE_DATASET,
        help=(
            "Path to the input CSV dataset."
            f"Defaults to '{DEFAULT_LOCATION_FILE_DATASET}' if not specified."
        ),
    )

    parser.add_argument(
        "--save",
        type=str,
        default=DEFAULT_LOCATION_HISTOGRAM_IMAGES,
        help=(
            "Save all the histograms into png files."
            f"Defaults to '{DEFAULT_LOCATION_FILE_DATASET}' if not specified."
        ),
    )

    args = parser.parse_args()

    try:
        data = pd.read_csv(args.path)
        df = data.dropna()

        for course in df:
            if not is_float_dtype(df[course]):
                continue

            plt.figure("Histogram", figsize=(10, 6))
            sns.histplot(
                data=df,
                x=course,
                hue="Hogwarts House",
                multiple="stack",
                stat="frequency",
            )

            plt.title(f"Histogram of {course} Scores by Hogwarts House")
            plt.xlabel(f"{course} Score")
            plt.ylabel("Frequency")

            if args.save:
                if not os.path.exists(DEFAULT_LOCATION_HISTOGRAM_IMAGES):
                    os.makedirs(DEFAULT_LOCATION_HISTOGRAM_IMAGES)
                plt.savefig(f"{DEFAULT_LOCATION_HISTOGRAM_IMAGES}/histplot_{course.lower()}.png")
                plt.close()
            else:
                plt.show()

    except FileNotFoundError:
        print(f"Error: File '{args.path}' not found.")
    except Exception as ex:
        print(f"Unexpected error occured : {ex}")
