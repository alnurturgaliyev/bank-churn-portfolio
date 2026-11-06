from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
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

# Read only the training data.
train = pd.read_csv(BASE_DIR / "data" / "modeling" / "train.csv")

X = train.drop(columns=["customer_id", "churned"])
y = train["churned"]

numeric_columns = ["age", "salary", "tenure", "balance"]
categorical_columns = ["gender", "geography", "num_products"]
binary_columns = ["has_credit_card", "is_active"]

# Keep the same preprocessing as the logistic regression comparison.
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
        RandomForestClassifier(
            n_estimators=300,
            max_depth=8,
            min_samples_leaf=10,
            class_weight="balanced",
            random_state=42,
            n_jobs=-1,
        ),
    ),
])

# Use the same folds as the baseline and logistic regression.
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

print("\nRandom forest: five-fold cross-validation")
print(summary.round(4))

summary.to_csv(
    REPORT_DIR / "random_forest_cv.csv",
    index_label="metric",
)
print("\nSaved reports/random_forest_cv.csv")
