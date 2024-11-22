import pandas as pd
import re


class CSVValidationError(Exception):
    pass


class ColumnMismatchError(CSVValidationError):
    pass


class ValueValidationError(CSVValidationError):
    pass


class DtypeMismatchError(CSVValidationError):
    pass


def validate_birthday_format(df):
    pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")

    if not df["Birthday"].apply(lambda x: bool(pattern.match(x))).all():
        return False

    return True


def validate_csv_values(df):
    if not df["Best Hand"].isin(["Right", "Left"]).all():
        return False

    if not df["Hogwarts House"].isin(["Gryffindor", "Ravenclaw", "Slytherin", "Hufflepuff"]).all():
        return False

    return True


def validate_csv_structure(df):
    expected_dtypes = {
        "Index": int,
        "Hogwarts House": object,
        "First Name": object,
        "Last Name": object,
        "Birthday": object,
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

    if list(df.columns) != list(expected_dtypes.keys()):
        raise ColumnMismatchError("Column names do not match the expected structure.")

    if not validate_csv_values(df):
        raise ValueValidationError("Invalid values found in 'Best Hand' or 'Hogwarts House'.")

    if not validate_birthday_format(df):
        raise ValueValidationError("Invalid 'Birthday' format, should be YYYY-MM-DD.")

    for col, dtype in expected_dtypes.items():
        if not pd.api.types.is_dtype_equal(df[col].dtype, dtype):
            raise DtypeMismatchError(
                f"Data type mismatch in column '{col}'. Expected {dtype}, found {df[col].dtype}."
            )

    return True
