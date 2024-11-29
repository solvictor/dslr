from utils import parse_csv, CSVValidationError, AVAILABLE_COURSES, DEFAULT_LOCATION_DATASET
import pickle
import numpy as np
import argparse
import csv


DEFAULT_OUTPUT_PREDICTION = "houses.csv"


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def predict(X, weights, biases):
    logits = np.dot(X, np.array(weights).T) + np.array(biases)
    probabilities = sigmoid(logits)
    predictions = np.argmax(probabilities, axis=1)

    return predictions


def load_model_from_pickle(model_file):
    with open(model_file, "rb") as f:
        model_data = pickle.load(f)
    return model_data


def parse_args():
    parser = argparse.ArgumentParser(
        prog="logreg_predict",
        description="Make predictions using a trained logistic regression model.",
    )

    parser.add_argument(
        "--model-file",
        type=str,
        required=True,
        help="Path to the .pkl file containing the trained model weights and biases.",
    )

    parser.add_argument(
        "--input-file",
        type=str,
        default=DEFAULT_LOCATION_DATASET,
        help=f"Path to the input dataset (CSV format) for making predictions. Defaults to '{DEFAULT_LOCATION_DATASET}' if not specified.",
    )

    parser.add_argument(
        "--output-file",
        type=str,
        default=DEFAULT_OUTPUT_PREDICTION,
        help=f"Path to the output file where predictions will be saved. Defaults to '{DEFAULT_OUTPUT_PREDICTION}' if not specified.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="If set, enables verbose mode for debugging purposes.",
    )

    return parser.parse_args()


def main():
    args = parse_args()

    try:
        data = parse_csv(args.input_file)
        X = np.array(data[AVAILABLE_COURSES].values)
        X = (X - np.mean(X, axis=0)) / np.std(X, axis=0)

        model_data = load_model_from_pickle(args.model_file)
        weights = model_data["weights"]
        biases = model_data["biases"]

        predictions = predict(X, weights, biases)

        predicted_houses = [
            {0: "Gryffindor", 1: "Hufflepuff", 2: "Ravenclaw", 3: "Slytherin"}[pred]
            for pred in predictions
        ]

        with open(args.output_file, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Index", "Hogwarts House"])
            for i, house in enumerate(predicted_houses):
                writer.writerow([i, house])

        print(f"Predictions saved to {args.output_file}")
        if args.verbose:
            accuracy = (
                np.mean(
                    predictions
                    == (
                        data["Hogwarts House"]
                        .map({"Gryffindor": 0, "Slytherin": 1, "Hufflepuff": 2, "Ravenclaw": 3})
                        .values
                    )
                )
                * 100
            )
            print(f"Accuracy: {accuracy}%")
    except FileNotFoundError:
        print(f"Error: File '{args.path}' not found.")
    except CSVValidationError as ex:
        print(f"{ex.__class__.__name__}: {ex}")
    except Exception as ex:
        print(f"Unexpected error occured : {ex}")


if __name__ == "__main__":
    main()
