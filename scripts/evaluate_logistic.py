from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    f1_score,
    make_scorer,
    precision_score,
    recall_score,
)
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

BASE_DIR = Path(__file__).resolve().parents[1]
REPORT_DIR = BASE_DIR / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

train = pd.read_csv(BASE_DIR / "data" / "modeling" / "train.csv")

X = train.drop(columns=["customer_id", "churned"])
y = train["churned"]

numeric_columns = ["age", "salary", "tenure", "balance"]
categorical_columns = ["gender", "geography", "num_products"]
binary_columns = ["has_credit_card", "is_active"]

numeric_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median", add_indicator=True)),
    ("scaler", StandardScaler()),
])

preprocessor = ColumnTransformer([
    ("numeric", numeric_pipeline, numeric_columns),
    (
        "categorical",
        OneHotEncoder(handle_unknown="ignore"),
        categorical_columns,
    ),
    ("binary", "passthrough", binary_columns),
])

model = Pipeline([
    ("preprocessor", preprocessor),
    (
        "classifier",
        LogisticRegression(
            class_weight="balanced",
            max_iter=1000,
            random_state=42,
        ),
    ),
])

cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42,
)

scoring = {
    "accuracy": "accuracy",
    "precision": make_scorer(precision_score, zero_division=0),
    "recall": make_scorer(recall_score, zero_division=0),
    "f1": make_scorer(f1_score, zero_division=0),
    "roc_auc": "roc_auc",
    "average_precision": "average_precision",
}

scores = cross_validate(
    model,
    X,
    y,
    cv=cv,
    scoring=scoring,
    error_score="raise",
)

summary = pd.DataFrame(
    {
        metric: {
            "mean": scores[f"test_{metric}"].mean(),
            "std": scores[f"test_{metric}"].std(),
        }
        for metric in scoring
    }
).T

print("\nLogistic regression: five-fold cross-validation")
print(summary.round(4))

summary.to_csv(REPORT_DIR / "logistic_cv.csv", index_label="metric")
print("\nSaved reports/logistic_cv.csv")
