import logging
import os
import pickle

import numpy as np
from flask import Flask, jsonify, request

with open("bin/dv_and_model.bin", mode="rb") as file:
    dv, model = pickle.load(file)

app = Flask("housing_prices")

logger = logging.getLogger(__name__)


@app.route("/")
def blank():
    return (
        "<!doctype html><html lang=en><meta charset=utf-8><title>This page intentionally left blank</title>"
        "<body><p>This page intentionally left blank"
    )


@app.route("/predict", methods=["POST"])
@app.errorhandler(400)
def predict():
    house = request.get_json()

    if not house:
        return jsonify(error="Empty requests are not supported"), 400

    # noinspection PyPep8Naming
    X = dv.transform([house])
    y_pred = model.predict(X)

    # Reverse the conversion of price from log value
    predicted_price = np.expm1(y_pred)[0]

    logger.debug(f"predicted price: {predicted_price}")

    # Round the result to cents
    result = {"price": round(float(predicted_price), 2)}

    return jsonify(result)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0")
