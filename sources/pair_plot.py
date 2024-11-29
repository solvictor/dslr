from argparse import ArgumentParser
from utils import (
    parse_csv,
    CSVValidationError,
    AVAILABLE_COURSES,
    HOUSE_COLORS,
    DEFAULT_LOCATION_DATASET,
)
from matplotlib import pyplot as plt
import matplotlib.lines as mlines
import seaborn as sns
import signal
import os


DEFAULT_LOCATION_IMAGES = "pair_plot"


if __name__ == "__main__":
    parser = ArgumentParser(
        prog="pair_plot",
        description="Pair plot of Hogwarts course scores for each house.",
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
        help="Save the pair plots into png files.",
    )

    parser.add_argument(
        "--save-folder",
        type=str,
        default=DEFAULT_LOCATION_IMAGES,
        help=f"Folder location of pair plots png files. Defaults to '{DEFAULT_LOCATION_IMAGES}' if not specified.",
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
        course_mapping = {
            "Arithmancy": "Arith",
            "Astronomy": "Astro",
            "Herbology": "Herb",
            "Defense Against the Dark Arts": "DADA",
            "Divination": "Div",
            "Muggle Studies": "Muggle",
            "Ancient Runes": "Runes",
            "History of Magic": "History",
            "Transfiguration": "Trans",
            "Potions": "Potions",
            "Care of Magical Creatures": "Creat",
            "Charms": "Charms",
            "Flying": "Flying",
        }

        df = df.rename(columns=course_mapping)

        pair_plot = sns.pairplot(
            df,
            vars=[course_mapping[course] for course in sorted(AVAILABLE_COURSES)],
            hue="Hogwarts House",
            palette=HOUSE_COLORS,
            plot_kws={"alpha": 0.7, "s": 10},
        )

        pair_plot._legend.remove()
        plt.legend(
            handles=[
                mlines.Line2D(
                    [0],
                    [0],
                    marker="o",
                    color="w",
                    markerfacecolor=color,
                    markersize=10,
                    label=house,
                )
                for house, color in HOUSE_COLORS.items()
            ],
            title="Hogwarts House",
            bbox_to_anchor=(1.1, len(AVAILABLE_COURSES) + 1),
            loc="upper left",
            borderaxespad=0.0,
        )
        pair_plot.figure.suptitle("Pair Plot of Hogwarts Courses by House")
        plt.gcf().canvas.manager.set_window_title("Hogwarts Courses Pair Plot")
        plt.subplots_adjust(top=0.95, right=0.9)

        for ax in pair_plot.axes.flatten():
            ax.set_xticks([])
            ax.set_yticks([])

        if args.save:
            if not os.path.exists(args.save_folder):
                os.makedirs(args.save_folder)
            pair_plot.savefig(f"{args.save_folder}/pairplot.png", bbox_inches="tight")

        plt.show()

    except FileNotFoundError:
        print(f"Error: File '{args.path}' not found.")
    except CSVValidationError as ex:
        print(f"{ex.__class__.__name__}: {ex}")
    except Exception as ex:
        print(f"Unexpected error occurred: {ex}")
