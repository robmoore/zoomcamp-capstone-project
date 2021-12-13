import pickle
from typing import Tuple

import numpy as np
import pandas as pd
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import ElasticNet
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

random_state = 42


def read_and_transform_data() -> Tuple[
    DictVectorizer, np.ndarray, np.ndarray, pd.DataFrame
]:
    df = pd.read_table(
        "data/AmesHousing.txt",
        index_col="PID",
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

    bmst_columns = [
        "bsmtfin_sf_1",
        "bsmtfin_sf_2",
        "bsmt_unf_sf",
        "total_bsmt_sf",
        "bsmt_full_bath",
        "bsmt_half_bath",
    ]

    mask = df["bsmt_qual"] == "NA"
    df.loc[mask, bmst_columns] = df.loc[mask, bmst_columns].fillna(0)

    df = df.drop(["order", "garage_yr_blt", "lot_frontage"], axis=1)

    df["mas_vnr_type"] = df["mas_vnr_type"].fillna("None")
    mask = (df["mas_vnr_type"] == "None") & (df["mas_vnr_area"].isna())
    df.loc[mask, "mas_vnr_area"] = df.loc[mask, "mas_vnr_area"].fillna(0.0)

    df.loc[916386080, "electrical"] = "SBrkr"

    # Based on author's comments, removing atypical examples
    df = df[df.gr_liv_area <= 4000]

    # Based on the author's comments, removing sales that fall outside of typical case (eg, ignoring foreclosures,
    # unfinished homes, and family sales) since those sales are not representative
    df = df[df.sale_condition == "Normal"]
    df = df.drop(["sale_condition"], axis=1)

    # Convert ordinal values to strings to aid in conversion below
    for col in ["ms_subclass", "overall_qual", "overall_cond"]:
        df[col] = df[col].astype("str")

    df_train, df_test = train_test_split(
        df,
        test_size=0.2,
        random_state=random_state,
    )

    df_train = df_train.reset_index(drop=True)
    df_test = df_test.reset_index(drop=True)

    y_train = np.log1p(df_train["saleprice"])
    df_train = df_train.drop(["saleprice"], axis=1)

    categorical_columns = list(df_train.dtypes[df_train.dtypes == "object"].index)
    numerical_columns = list(df_train.dtypes[df_train.dtypes != "object"].index)

    dv = DictVectorizer(sparse=False)
    dv.fit(df[categorical_columns + numerical_columns].to_dict(orient="records"))

    train_dict = df_train[categorical_columns + numerical_columns].to_dict(
        orient="records"
    )
    # noinspection PyPep8Naming
    X_train = dv.transform(train_dict)

    return dv, X_train, y_train, df_test


# noinspection PyPep8Naming
def create_model(X_train: np.ndarray, y_train: np.ndarray):
    return Pipeline(
        [
            ("scale", StandardScaler()),
            (
                "regr",
                ElasticNet(
                    alpha=0.01, l1_ratio=0.1, max_iter=2000, random_state=random_state
                ),
            ),
        ]
    ).fit(X_train, y_train)


def main():
    # noinspection PyPep8Naming
    dict_vectorizer, X, y, df_test = read_and_transform_data()
    model = create_model(X, y)

    with open("bin/dv_and_model.bin", "wb") as dv_and_model_bin:
        pickle.dump((dict_vectorizer, model), dv_and_model_bin)

    df_test.to_pickle("bin/test.bin")


if __name__ == "__main__":
    main()
