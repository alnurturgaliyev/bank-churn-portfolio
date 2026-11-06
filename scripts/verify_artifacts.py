"""Check saved splits, predictions, metrics, and the locally fitted pipeline."""

from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score, average_precision_score, confusion_matrix, f1_score,
    precision_score, recall_score, roc_auc_score,
)

root = Path(__file__).resolve().parents[1]
train = pd.read_csv(root / "data/modeling/train.csv")
test = pd.read_csv(root / "data/modeling/test.csv")
predictions = pd.read_csv(root / "reports/final_test_predictions.csv")
metrics = pd.read_csv(root / "reports/final_test_metrics.csv", index_col="metric")["value"]
matrix = pd.read_csv(root / "reports/final_test_confusion_matrix.csv", index_col=0)

assert (len(train), len(test)) == (8000, 2000)
assert train.customer_id.is_unique and test.customer_id.is_unique
assert set(train.customer_id).isdisjoint(test.customer_id)
assert train.balance.isna().sum() + test.balance.isna().sum() == 3617
np.testing.assert_array_equal(test.customer_id, predictions.customer_id)
np.testing.assert_array_equal(test.churned, predictions.actual_churned)

y = test.churned
p = predictions.predicted_churned
s = predictions.churn_score
computed = {
    "accuracy": accuracy_score(y, p),
    "precision": precision_score(y, p, zero_division=0),
    "recall": recall_score(y, p, zero_division=0),
    "f1": f1_score(y, p, zero_division=0),
    "roc_auc": roc_auc_score(y, s),
    "average_precision": average_precision_score(y, s),
}
for name, value in computed.items():
    np.testing.assert_allclose(metrics[name], value, rtol=1e-12, atol=1e-12)
np.testing.assert_array_equal(matrix.to_numpy(), confusion_matrix(y, p, labels=[0, 1]))

# Replay saved predictions, without fitting or altering any model choices.
model = joblib.load(root / "models/churn_random_forest.joblib")
X = test[list(model.feature_names_in_)]
np.testing.assert_array_equal(model.predict(X), p)
column = list(model.classes_).index(1)
np.testing.assert_allclose(model.predict_proba(X)[:, column], s, rtol=1e-12, atol=1e-12)
print("Verified: split sizes, unique/disjoint customer IDs, missing balances,")
print("prediction alignment, six test metrics, confusion matrix, and saved-model replay.")
