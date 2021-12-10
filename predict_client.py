import argparse

import numpy as np
import pandas as pd
import requests as requests
from numpy.random import default_rng

SEED = 42
URL = "http://0.0.0.0:5000/predict"


def main(url: str) -> tuple[float, float]:
    df = pd.read_pickle("bin/test.bin")
    # noinspection PyPep8Naming
    X, y = df.drop("saleprice", axis=1), df["saleprice"]

    rng = default_rng(SEED)
    index = rng.integers(len(df))

    house = X.iloc[index].to_dict()
    result = requests.post(url, json=house).json()

    return result["price"], y[index]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-u",
        "--url",
        help="URL of service endpoint",
        type=str,
        default=URL,
    )

    args = parser.parse_args()

    predicted_price, actual_price = main(args.url)
    # Remember to reverse conversion of price to log value
    predicted_price = round(np.expm1(predicted_price))

    print(f"predicted price: {predicted_price}; actual price: {actual_price}")
