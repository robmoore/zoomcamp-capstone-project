import numpy as np
import pandas as pd
import requests as requests
from numpy.random import default_rng

SEED = 42
# URL = "http://0.0.0.0:5000/predict"
URL = "https://zoomcamp-capstone.herokuapp.com/predict"

df = pd.read_pickle("test.bin")
X, y = df.drop("saleprice", axis=1), df["saleprice"]

rng = default_rng(SEED)
index = rng.integers(len(df))

house = X.iloc[index].to_dict()
# TODO reverse log conversion on price
print(requests.post(URL, json=house).json(), np.log1p(y[index]))
