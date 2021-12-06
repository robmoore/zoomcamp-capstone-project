import pickle

import inflection
from sklearn.feature_extraction import DictVectorizer
import xgboost as xgb
import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np

random_state = 42


def read_and_transform_data() -> tuple[DictVectorizer, np.ndarray, np.ndarray]:
    df = pd.read_table(
        "AmesHousing.csv",
        index_col="Order",
    )

    df.columns = df.columns.str.lower().str.replace(" ", "_")

    df["central_air"] = df["central_air"] == "Y"
    df["paved_drive"] = df["paved_drive"] == "Y"

    na_columns = [
        "alley",
        "bsmt_qual",
        "bsmt_cond",
        "bsmt_exposure",
        "bsmtfin_type_1",
        "bsmtfin_type_2",
        "fireplace_qu",
        "garage_type",
        "garage_finish",
        "garage_qual",
        "garage_cond",
        "pool_qc",
        "fence",
        "misc_feature",
    ]
    df[na_columns] = df[na_columns].fillna("NA")

    df = df.dropna()
    df[["lot_frontage", "garage_yr_blt"]] = df[
        ["lot_frontage", "garage_yr_blt"]
    ].astype(int)

    df_train, df_test = train_test_split(
        df,
        test_size=0.2,
        random_state=random_state,
    )

    df_train = df_train.reset_index(drop=True)

    categorical_columns = list(df_train.dtypes[df_train.dtypes == "object"].index)

    numerical_columns = list(df_train.dtypes[df_train.dtypes != "object"].index)
    numerical_columns = [
        column for column in numerical_columns if column != "sale_price"
    ]

    y_train = np.log1p(df_train["sale_price"])

    columns_to_drop = ["sale_price", "pid"]

    categorical_columns = [
        column for column in categorical_columns if column not in columns_to_drop
    ]
    df_train = df_train.drop(columns_to_drop, axis=1)

    dv = DictVectorizer(sparse=False)
    dv.fit(df[categorical_columns + numerical_columns].to_dict(orient="records"))

    train_dict = df_train[categorical_columns + numerical_columns].to_dict(
        orient="records"
    )
    # noinspection PyPep8Naming
    X_train = dv.transform(train_dict)

    return dv, X_train, y_train


# noinspection PyPep8Naming
def create_model(X_train: np.ndarray, y_train: np.ndarray) -> xgb.XGBRegressor:
    return xgb.XGBRegressor(
        random_state=random_state,
        n_jobs=-1,
        learning_rate=0.1,
        max_depth=4,
        min_child_weight=1,
        subsample=0.8,
    ).fit(X_train, y_train)


dict_vectorizer, X, y = read_and_transform_data()
model = create_model(X, y)

with open("dv_and_model.bin", "wb") as dv_and_model_bin:
    pickle.dump((dict_vectorizer, model), dv_and_model_bin)
