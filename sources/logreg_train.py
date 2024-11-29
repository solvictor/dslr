from utils import parse_csv, AVAILABLE_COURSES
import numpy as np


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def compute_cost(y, y_pred):
    return -(1 / len(y)) * np.sum(y * np.log(y_pred) + (1 - y) * np.log(1 - y_pred))


def gradient_descent_binary(X, y, weights, bias, learning_rate, epochs):
    m = X.shape[0]

    for i in range(epochs):
        z = np.dot(X, weights) + bias
        y_pred = sigmoid(z)

        dw = (1 / m) * np.dot(X.T, (y_pred - y))
        db = (1 / m) * np.sum(y_pred - y)

        weights -= learning_rate * dw
        bias -= learning_rate * db

    return weights, bias


def train_logistic_regression_ovr(X, y, num_classes, learning_rate=0.01, epochs=10000):
    n_features = X.shape[1]

    all_weights = np.zeros((num_classes, n_features))
    all_biases = np.zeros(num_classes)

    for i in range(num_classes):
        binary_y = np.where(y == i, 1, 0)

        weights = np.zeros(n_features)
        bias = 0

        weights, bias = gradient_descent_binary(X, binary_y, weights, bias, learning_rate, epochs)

        all_weights[i:] = weights
        all_biases[i] = bias

    return all_weights, all_biases


# def predict_ovr(X, all_weights, all_biases):
#     scores = np.dot(X, all_weights.T) + all_biases
#     y_pred = sigmoid(scores)

#     return np.argmax(y_pred, axis=1)


data = parse_csv("data/dataset_train.csv")

X = np.array(data[AVAILABLE_COURSES].values)

houses = {"Gryffindor": 0, "Slytherin": 1, "Hufflepuff": 2, "Ravenclaw": 3}
y = data["Hogwarts House"].map(houses).values

X = (X - np.mean(X, axis=0)) / np.std(X, axis=0)

num_classes = 4
all_weights, all_biases = train_logistic_regression_ovr(
    X, y, num_classes, learning_rate=0.01, epochs=10_000
)

print(all_weights, all_biases)

# predictions = predict_ovr(X, all_weights, all_biases)

# accuracy = np.mean(predictions == y) * 100
# print(f"Accuracy: {accuracy}%")
