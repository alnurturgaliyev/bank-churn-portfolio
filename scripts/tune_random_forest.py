import json
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
from sklearn.model_selection import GridSearchCV, StratifiedKFold
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
            class_weight="balanced",
            random_state=42,
            n_jobs=-1,
        ),
    ),
])

# 2 × 2 × 2 = 8 configurations.
param_grid = {
    "classifier__max_depth": [8, 12],
    "classifier__min_samples_leaf": [5, 10],
    "classifier__max_features": ["sqrt", 0.7],
}

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

search = GridSearchCV(
    estimator=model,
    param_grid=param_grid,
    scoring=scoring,
    refit="f1",
    cv=cv,
    n_jobs=1,
    verbose=1,
    error_score="raise",
)

search.fit(X, y)

results = pd.DataFrame(search.cv_results_)
results.sort_values("rank_test_f1").to_csv(
    REPORT_DIR / "random_forest_search.csv",
    index=False,
)

best_index = search.best_index_

summary = pd.DataFrame(
    {
        metric: {
            "mean": results.loc[best_index, f"mean_test_{metric}"],
            "std": results.loc[best_index, f"std_test_{metric}"],
        }
        for metric in scoring
    }
).T

summary.to_csv(
    REPORT_DIR / "random_forest_tuned_cv.csv",
    index_label="metric",
)

with (REPORT_DIR / "random_forest_best_params.json").open("w") as file:
    json.dump(search.best_params_, file, indent=2)

print("\nBest parameters:")
print(json.dumps(search.best_params_, indent=2))

print("\nCross-validation results for the selected configuration:")
print(summary.round(4))

print("\nSaved search results, selected metrics, and best parameters.")
print("The reserved test file was not used.")
