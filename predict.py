import pickle

from flask import Flask, request, jsonify
from sklearn.feature_extraction import DictVectorizer
import xgboost as xgb

with open("dv.bin", mode="rb") as file:
    dv: DictVectorizer = pickle.load(file)
with open("model1.bin", mode="rb") as file:
    model: xgb.XGBRegressor = pickle.load(file)

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
    app.run(debug=True, host="0.0.0.0")