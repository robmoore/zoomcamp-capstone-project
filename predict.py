import os
import pickle

from flask import Flask, jsonify, request

with open("bin/dv_and_model.bin", mode="rb") as file:
    dv, model = pickle.load(file)

app = Flask("housing_prices")


@app.route("/predict", methods=["POST"])
def predict():
    house = request.get_json()

    # noinspection PyPep8Naming
    X = dv.transform([house])
    y_pred = model.predict(X)[0]

    result = {"price": float(y_pred)}

    return jsonify(result)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0")
