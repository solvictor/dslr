from utils import parse_csv, CSVValidationError, AVAILABLE_COURSES, DEFAULT_LOCATION_DATASET_TRAIN
from argparse import ArgumentParser
import numpy as np
import pickle


NUMBER_OF_HOUSES = 4
DEFAULT_LOCATION_JSON = "weights.pkl"


def parse_args():
    parser = ArgumentParser(
        prog="logreg_train",
        description="Train a logistic regression model using One-vs-Rest (OvR) method.",
    )

    parser.add_argument(
        "--epochs", type=int, default=1_000, help="Number of epochs for training the model."
    )

    parser.add_argument(
        "--learning_rate",
        type=float,
        default=0.001,
        help="Learning rate to use for gradient descent.",
    )

    parser.add_argument(
        "--input-file",
        type=str,
        default=DEFAULT_LOCATION_DATASET_TRAIN,
        help=f"Path to the input CSV dataset. Defaults to '{DEFAULT_LOCATION_DATASET_TRAIN}' if not specified.",
    )

    parser.add_argument(
        "--output_file",
        type=str,
        default=DEFAULT_LOCATION_JSON,
        help=f"Path to the output JSON file where model weights and biases will be saved. Defaults to '{DEFAULT_LOCATION_JSON}' if not specified.",
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="If set, enables verbose mode for debugging purposes.",
    )

    parser.add_argument(
        "--optimizer",
        choices=["gd", "minibatch", "sgd"],
        default="gd",
        help="Choose the optimization method: 'gd' for full batch gradient descent, 'minibatch' for mini-batch gradient descent, or 'sgd' for stochastic gradient descent.",
    )

    return parser.parse_args()


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def compute_cost(y, y_pred):
    return -(1 / len(y)) * np.sum(y * np.log(y_pred) + (1 - y) * np.log(1 - y_pred))


def gradient_descent_binary(X, y, weights, bias, learning_rate, epochs, batch):
    m = X.shape[0]

    for i in range(epochs):
        for j in range(0, m, batch):
            X_batch = X[j : j + batch]
            y_batch = y[j : j + batch]

            z = np.dot(X_batch, weights) + bias
            y_pred = sigmoid(z)

            dw = np.dot(X_batch.T, (y_pred - y_batch)) / batch
            db = np.sum(y_pred - y_batch) / batch

            weights -= learning_rate * dw
            bias -= learning_rate * db

    return weights, bias


def train_logistic_regression_ovr(X, y, num_classes, learning_rate, epochs, batch):
    n_features = X.shape[1]

    all_weights = np.zeros((num_classes, n_features))
    all_biases = np.zeros(num_classes)

    for i in range(num_classes):
        binary_y = np.where(y == i, 1, 0)

        weights = np.zeros(n_features)
        bias = 0

        weights, bias = gradient_descent_binary(
            X, binary_y, weights, bias, learning_rate, epochs, batch
        )

        all_weights[i:] = weights
        all_biases[i] = bias

    return all_weights, all_biases


def save_model_to_pickle(weights, biases, output_file):
    model_data = {
        "weights": weights,
        "biases": biases,
    }

    with open(output_file, "wb") as f:
        pickle.dump(model_data, f)


def main():
    args = parse_args()

    try:
        data = parse_csv(args.input_file)

        X = np.array(data[AVAILABLE_COURSES].values)
        y = (
            data["Hogwarts House"]
            .map({"Gryffindor": 0, "Slytherin": 1, "Hufflepuff": 2, "Ravenclaw": 3})
            .values
        )

        X = (X - np.mean(X, axis=0)) / np.std(X, axis=0)

        weights, biases = train_logistic_regression_ovr(
            X, y, NUMBER_OF_HOUSES, args.learning_rate, args.epochs, 64
        )

        save_model_to_pickle(weights, biases, args.output_file)
    except FileNotFoundError:
        print(f"Error: File '{args.path}' not found.")
    except CSVValidationError as ex:
        print(f"{ex.__class__.__name__}: {ex}")
    except Exception as ex:
        print(f"Unexpected error occured : {ex}")


if __name__ == "__main__":
    main()
