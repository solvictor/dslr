from argparse import ArgumentParser
from itertools import combinations
from utils import parse_csv, CSVValidationError, AVAILABLE_COURSES
from matplotlib import pyplot as plt
import seaborn as sns
import signal
import os


DEFAULT_LOCATION_IMAGES = "scatterplots"
DEFAULT_LOCATION_DATASET = "data/dataset_train.csv"
MOST_SIMILAR_FEATURES = ("Astronomy", "Defense Against the Dark Arts")


if __name__ == "__main__":
    parser = ArgumentParser(
        prog="scatter_plot",
        description="Plot scatter plots of each Hogwarts course scores against another course, for each house.",
    )

    parser.add_argument(
        "--path",
        type=str,
        default=DEFAULT_LOCATION_DATASET,
        help=f"Path to the input CSV dataset. Defaults to '{DEFAULT_LOCATION_DATASET}' if not specified.",
    )

    parser.add_argument(
        "--save",
        action="store_true",
        help="Save all the scatter plots into png files.",
    )

    parser.add_argument(
        "--show",
        action="store_true",
        help="Show all the scatter plots.",
    )

    parser.add_argument(
        "--save-folder",
        type=str,
        default=DEFAULT_LOCATION_IMAGES,
        help=f"Folder location of scatter plots png files. Defaults to '{DEFAULT_LOCATION_DATASET}' if not specified.",
    )

    args = parser.parse_args()

    if args.save_folder != DEFAULT_LOCATION_IMAGES:
        args.save = True

    try:
        signal.signal(
            signal.SIGINT,
            lambda *_: (print("\033[2Ddslr: CTRL+C sent by user."), exit(1)),
        )

        df = parse_csv(args.path)

        for first_course, second_course in combinations(sorted(AVAILABLE_COURSES), r=2):
            if args.save or args.show or (first_course, second_course) == MOST_SIMILAR_FEATURES:
                plt.figure("Scatter plot", figsize=(10, 6))
                sns.scatterplot(
                    data=df,
                    x=df[first_course],
                    y=df[second_course],
                    hue="Hogwarts House",
                    palette={
                        "Gryffindor": "#7F0909",
                        "Slytherin": "#1A472A",
                        "Hufflepuff": "#FFDB00",
                        "Ravenclaw": "#0E1A40",
                    },
                )

                plt.title(
                    f"Scatter plot of {first_course} against {second_course} Scores by Hogwarts House"
                )
                plt.xlabel(f"{first_course} Scores")
                plt.ylabel(f"{second_course} Scores")

                if args.save:
                    if not os.path.exists(args.save_folder):
                        os.makedirs(args.save_folder)
                    plt.savefig(
                        f"{args.save_folder}/scatterplot_{first_course.lower()}_{second_course.lower()}.png"
                    )
                if args.show or (first_course, second_course) == MOST_SIMILAR_FEATURES:
                    plt.show()
                else:
                    plt.close()

    except FileNotFoundError:
        print(f"Error: File '{args.path}' not found.")
    except CSVValidationError as ex:
        print(f"{ex.__class__.__name__}: {ex}")
    except Exception as ex:
        print(f"Unexpected error occured : {ex}")
