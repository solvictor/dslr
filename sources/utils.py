import pandas as pd


DEFAULT_LOCATION_DATASET_TRAIN = "data/dataset_train.csv"

AVAILABLE_COURSES = [
    "Arithmancy",
    "Astronomy",
    "Herbology",
    "Defense Against the Dark Arts",
    "Divination",
    "Muggle Studies",
    "Ancient Runes",
    "History of Magic",
    "Transfiguration",
    "Potions",
    "Care of Magical Creatures",
    "Charms",
    "Flying",
]

HOUSE_COLORS = {
    "Gryffindor": "#D62728",
    "Hufflepuff": "#ECB939",
    "Ravenclaw": "#1F77B4",
    "Slytherin": "#2CA02C",
}


class CSVValidationError(Exception):
    pass


class ColumnMismatchError(CSVValidationError):
    pass


class ValueValidationError(CSVValidationError):
    pass


class DtypeMismatchError(CSVValidationError):
    pass


def validate_csv_values(df, predict):
    if not df["Best Hand"].isin(["Right", "Left"]).all():
        return False

    if predict:
        return True

    if not df["Hogwarts House"].isin(["Gryffindor", "Ravenclaw", "Slytherin", "Hufflepuff"]).all():
        return False

    return True


def validate_csv_structure(df, predict):
    expected_dtypes = {
        "Hogwarts House": object,
        "First Name": object,
        "Last Name": object,
        "Birthday": "datetime64[ns]",
        "Best Hand": object,
        "Arithmancy": float,
        "Astronomy": float,
        "Herbology": float,
        "Defense Against the Dark Arts": float,
        "Divination": float,
        "Muggle Studies": float,
        "Ancient Runes": float,
        "History of Magic": float,
        "Transfiguration": float,
        "Potions": float,
        "Care of Magical Creatures": float,
        "Charms": float,
        "Flying": float,
    }

    if predict:
        expected_dtypes.pop("Hogwarts House")

    if list(df.columns) != list(expected_dtypes.keys()):
        raise ColumnMismatchError("Column names do not match the expected structure.")
    if not validate_csv_values(df, predict):
        raise ValueValidationError("Invalid values found in 'Best Hand' or 'Hogwarts House'.")

    for col, dtype in expected_dtypes.items():
        if not pd.api.types.is_dtype_equal(df[col].dtype, dtype):
            if col == "Birthday":
                raise ValueValidationError("Invalid 'Birthday' format, should be valid YYYY-MM-DD.")
            raise DtypeMismatchError(
                f"Data type mismatch in column '{col}'. Expected {dtype}, found {df[col].dtype}."
            )

    return True


def parse_csv(path, predict=False):
    data = pd.read_csv(path, index_col="Index", parse_dates=["Birthday"], date_format="%Y-%m-%d")
    if predict:
        data = data.drop(columns="Hogwarts House")
    validate_csv_structure(data, predict)

    return data if predict else data.dropna()
