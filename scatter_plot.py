from argparse import ArgumentParser
from itertools import combinations
from utils import parse_csv, CSVValidationError, AVAILABLE_COURSES
from matplotlib import pyplot as plt
import seaborn as sns


DEFAULT_LOCATION_IMAGES = "histograms"
DEFAULT_LOCATION_DATASET = "data/dataset_train.csv"


if __name__ == "__main__":
    parser = ArgumentParser(
        prog="scatter_plot",
        description="Plot scatter plots of each Hogwarts course scores against another course, for each house.",
    )

    parser.add_argument(
        "--path",
        type=str,
        default=DEFAULT_LOCATION_DATASET,
        help=(
            f"Path to the input CSV dataset. Defaults to '{DEFAULT_LOCATION_DATASET}' if not specified."
        ),
    )

    parser.add_argument(
        "--save",
        action="store_true",
        help=("Save all the scatter plots into png files."),
    )

    parser.add_argument(
        "--show",
        action="store_true",
        help=("Show all the scatter plots plots."),
    )

    parser.add_argument(
        "--save-folder",
        type=str,
        default=DEFAULT_LOCATION_IMAGES,
        help=(
            "Folder location of scatter plots png files."
            f"Defaults to '{DEFAULT_LOCATION_DATASET}' if not specified."
        ),
    )

    args = parser.parse_args()

    if args.save_folder != DEFAULT_LOCATION_IMAGES:
        args.save = True

    try:
        df = parse_csv(args.path)

        for first_course, second_course in combinations(sorted(AVAILABLE_COURSES), r=2):
            if first_course not in df or second_course not in df:
                continue

            plt.figure("Scatter plot", figsize=(10, 6))
            sns.scatterplot(
                data=df,
                x=df[first_course],
                y=df[second_course],
                hue="Hogwarts House",
            )

            plt.title(
                f"Scatter plot of {first_course} against {second_course} Scores by Hogwarts House"
            )
            plt.xlabel("Score")
            plt.ylabel("Count")
            plt.show()

    except FileNotFoundError:
        print(f"Error: File '{args.path}' not found.")
    except CSVValidationError as ex:
        print(f"{ex.__class__.__name__}: {ex}")
    except Exception as ex:
        print(f"Unexpected error occured : {ex}")
