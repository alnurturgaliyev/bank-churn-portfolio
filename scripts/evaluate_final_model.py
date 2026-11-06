import json
from pathlib import Path

import joblib
import pandas as pd
import sklearn
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data" / "modeling"
REPORT_DIR = BASE_DIR / "reports"
MODEL_DIR = BASE_DIR / "models"

REPORT_DIR.mkdir(parents=True, exist_ok=True)
MODEL_DIR.mkdir(parents=True, exist_ok=True)

train = pd.read_csv(DATA_DIR / "train.csv")
test = pd.read_csv(DATA_DIR / "test.csv")

assert train["customer_id"].is_unique
assert test["customer_id"].is_unique
assert set(train["customer_id"]).isdisjoint(test["customer_id"])

X_train = train.drop(columns=["customer_id", "churned"])
y_train = train["churned"]

X_test = test[X_train.columns]
y_test = test["churned"]

with (REPORT_DIR / "random_forest_best_params.json").open() as file:
    best_params = json.load(file)

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

model.set_params(**best_params)

# Fit preprocessing and the classifier using training rows only.
print("Fitting the selected pipeline on all training rows...")
model.fit(X_train, y_train)

joblib.dump(model, MODEL_DIR / "churn_random_forest.joblib")

# Evaluate the fixed model on the reserved test portion.
predictions = model.predict(X_test)
churn_column = list(model.classes_).index(1)
scores = model.predict_proba(X_test)[:, churn_column]

metrics = pd.Series({
    "accuracy": accuracy_score(y_test, predictions),
    "precision": precision_score(y_test, predictions, zero_division=0),
    "recall": recall_score(y_test, predictions, zero_division=0),
    "f1": f1_score(y_test, predictions, zero_division=0),
    "roc_auc": roc_auc_score(y_test, scores),
    "average_precision": average_precision_score(y_test, scores),
}, name="value")

matrix = confusion_matrix(y_test, predictions, labels=[0, 1])
matrix_table = pd.DataFrame(
    matrix,
    index=["actual_retained", "actual_churned"],
    columns=["predicted_retained", "predicted_churned"],
)

metrics.rename_axis("metric").to_csv(
    REPORT_DIR / "final_test_metrics.csv"
)
matrix_table.to_csv(
    REPORT_DIR / "final_test_confusion_matrix.csv",
    index_label="actual",
)

pd.DataFrame({
    "customer_id": test["customer_id"],
    "actual_churned": y_test,
    "predicted_churned": predictions,
    "churn_score": scores,
}).to_csv(
    REPORT_DIR / "final_test_predictions.csv",
    index=False,
)

metadata = {
    "model": "RandomForestClassifier",
    "selected_parameters": best_params,
    "n_estimators": 300,
    "class_weight": "balanced",
    "random_state": 42,
    "classification_threshold": 0.5,
    "training_rows": len(train),
    "test_rows": len(test),
    "feature_columns": X_train.columns.tolist(),
    "sklearn_version": sklearn.__version__,
    "scores_calibrated": False,
}

with (MODEL_DIR / "model_metadata.json").open("w") as file:
    json.dump(metadata, file, indent=2)

print(f"\nFinal evaluation on {len(test)} test customers:")
print(metrics.round(4))

print("\nConfusion matrix:")
print(matrix_table.to_string())

tn, fp, fn, tp = matrix.ravel()
print(f"\nCorrectly identified churners: {tp}")
print(f"Missed churners: {fn}")
print(f"False alarms: {fp}")
print(f"Correctly identified retained customers: {tn}")

print("\nSaved fitted pipeline and metadata in models/")
print("Saved test metrics, confusion matrix, and predictions in reports/")
