from argparse import ArgumentParser
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

if __name__ == "__main__":
    parser = ArgumentParser(
        prog="histogram",
        description="Plot histograms of Hogwarts course scores for each house.",
    )

    parser.add_argument(
        "--path",
        type=str,
        default="data/dataset_train.csv",
        help=(
            "Path to the input CSV dataset."
            "Defaults to 'data/dataset_train.csv' if not specified."
        ),
    )

    args = parser.parse_args()

    try:
        data = pd.read_csv(args.path)
        df = data.dropna()

        mn_val = int(df["Arithmancy"].min())
        mx_val = int(df["Arithmancy"].max())

        plt.figure(figsize=(10, 6))
        sns.histplot(
            data=df,
            x="Arithmancy",
            hue="Hogwarts House",
            bins=range(mn_val, mx_val + int(mx_val * 0.1), 4000),
            multiple="stack",
            stat="frequency",
        )

        plt.title("Histogram of Arithmancy Scores by Hogwarts House")
        plt.xlabel("Arithmancy Score")
        plt.ylabel("Frequency")

        plt.show()

    except FileNotFoundError:
        print(f"Error: File '{args.path}' not found.")
    except Exception as ex:
        print(f"Unexpected error occured : {ex}")
