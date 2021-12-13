import argparse
import logging
from typing import Tuple

import pandas as pd
import requests as requests
from numpy.random import default_rng

URL = "http://0.0.0.0:5000/predict"

logger = logging.getLogger(__name__)


def main(url: str) -> Tuple[float, float]:
    df = pd.read_pickle("bin/test.bin")
    # noinspection PyPep8Naming
    X, y = df.drop("saleprice", axis=1), df["saleprice"]

    rng = default_rng()
    index = rng.integers(len(df))

    house = X.iloc[index].to_dict()
    response = requests.post(url, json=house)
    logger.debug(f"request: {response.request.body}")
    logger.debug(f"response: {response.content}")

    return response.json()["price"], y[index]


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

    print(f"predicted price: {predicted_price}; actual price: {actual_price}")
