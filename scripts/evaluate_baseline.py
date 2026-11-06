from pathlib import Path

import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.metrics import (
    f1_score,
    make_scorer,
    precision_score,
    recall_score,
)
from sklearn.model_selection import StratifiedKFold, cross_validate

BASE_DIR = Path(__file__).resolve().parents[1]
REPORT_DIR = BASE_DIR / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

train = pd.read_csv(BASE_DIR / "data" / "modeling" / "train.csv")
y = train["churned"]

# The dummy model ignores features; give it a placeholder column.
X = pd.DataFrame({"placeholder": [0] * len(train)})

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
    DummyClassifier(strategy="prior"),
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

print("\nDummy baseline: five-fold cross-validation on training data")
print(summary.round(4))

summary.to_csv(REPORT_DIR / "baseline_cv.csv", index_label="metric")
print("\nSaved reports/baseline_cv.csv")
