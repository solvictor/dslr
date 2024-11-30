from utils import parse_csv, CSVValidationError, AVAILABLE_COURSES
import pickle
import numpy as np
import argparse
import csv


DEFAULT_LOCATION_DATASET_TEST = "data/dataset_test.csv"
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
        default=DEFAULT_LOCATION_DATASET_TEST,
        help=f"Path to the input dataset (CSV format) for making predictions. Defaults to '{DEFAULT_LOCATION_DATASET_TEST}' if not specified.",
    )

    parser.add_argument(
        "--output-file",
        type=str,
        default=DEFAULT_OUTPUT_PREDICTION,
        help=f"Path to the output file where predictions will be saved. Defaults to '{DEFAULT_OUTPUT_PREDICTION}' if not specified.",
    )

    return parser.parse_args()


def main():
    args = parse_args()

    try:
        data = parse_csv(args.input_file, predict=True)

        X = np.array(data[AVAILABLE_COURSES].values)

        # Replace NaN values with mean of courses, so after it will be 0 in the normalized vector X with standardization
        nan_mask = np.isnan(X)
        mean_values = np.nanmean(X, axis=0)
        X[nan_mask] = np.take(mean_values, np.where(nan_mask)[1])

        X = (X - np.mean(X, axis=0)) / np.std(X, axis=0)

        model_data = load_model_from_pickle(args.model_file)
        weights = model_data["weights"]
        biases = model_data["biases"]

        predictions = predict(X, weights, biases)
        predicted_houses = [
            {0: "Gryffindor", 1: "Slytherin", 2: "Hufflepuff", 3: "Ravenclaw"}[pred]
            for pred in predictions
        ]

        with open(args.output_file, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Index", "Hogwarts House"])
            for i, house in enumerate(predicted_houses):
                writer.writerow([i, house])

        print(f"Predictions saved to {args.output_file}")

    except FileNotFoundError:
        print(f"Error: File '{args.path}' not found.")
    except CSVValidationError as ex:
        print(f"{ex.__class__.__name__}: {ex}")
    except Exception as ex:
        print(f"Unexpected error occured : {ex}")


if __name__ == "__main__":
    main()
