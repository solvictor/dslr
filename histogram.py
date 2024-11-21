from argparse import ArgumentParser
from pandas.api.types import is_float_dtype
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


DEFAULT_LOCATION_HISTOGRAM_IMAGES = "histograms"
DEFAULT_LOCATION_FILE_DATASET = "data/dataset_train.csv"
MOST_HOMOGENOUS_FEATURE = "Arithmancy"


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
        action="store_true",
        help=("Save all the histograms into png files."),
    )

    parser.add_argument(
        "--show",
        action="store_true",
        help=("Show all the histograms plots."),
    )

    parser.add_argument(
        "--save-folder",
        type=str,
        default=DEFAULT_LOCATION_HISTOGRAM_IMAGES,
        help=(
            "Folder location of histograms png files."
            f"Defaults to '{DEFAULT_LOCATION_FILE_DATASET}' if not specified."
        ),
    )

    args = parser.parse_args()

    if args.save_folder != DEFAULT_LOCATION_HISTOGRAM_IMAGES:
        args.save = True

    try:
        data = pd.read_csv(args.path)
        df = data.dropna()

        for course in df:
            if not is_float_dtype(df[course]):
                continue

            if args.save or args.show or course == MOST_HOMOGENOUS_FEATURE:
                plt.figure("Histogram", figsize=(10, 6))

                sns.histplot(
                    data=df,
                    x=course,
                    hue="Hogwarts House",
                    multiple="stack",
                    stat="frequency",
                    palette={
                        "Gryffindor": "#7F0909",
                        "Slytherin": "#1A472A",
                        "Hufflepuff": "#FFDB00",
                        "Ravenclaw": "#0E1A40",
                    },
                )

                plt.title(f"Histogram of {course} Scores by Hogwarts House")
                plt.xlabel(f"{course} Score")
                plt.ylabel("Frequency")

                if args.save:
                    if not os.path.exists(args.save_folder):
                        os.makedirs(args.save_folder)
                    plt.savefig(f"{args.save_folder}/histplot_{course.lower()}.png")
                if args.show or course == MOST_HOMOGENOUS_FEATURE:
                    plt.show()
                else:
                    plt.close()

    except FileNotFoundError:
        print(f"Error: File '{args.path}' not found.")
    except Exception as ex:
        print(f"Unexpected error occured : {ex}")
