"""Score a CSV using the saved pipeline without fitting or changing the model."""

import argparse
from pathlib import Path

import joblib
import pandas as pd


def main():
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="CSV with the nine model features")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--model", type=Path,
        default=root / "models" / "churn_random_forest.joblib",
        help="Path to your locally generated model",
    )
    args = parser.parse_args()

    model = joblib.load(args.model)
    frame = pd.read_csv(args.input)
    features = list(model.feature_names_in_)
    missing = sorted(set(features) - set(frame.columns))
    if missing:
        parser.error(f"Input CSV is missing columns: {', '.join(missing)}")

    X = frame[features]
    result = frame[["customer_id"]].copy() if "customer_id" in frame else pd.DataFrame(index=frame.index)
    churn_column = list(model.classes_).index(1)
    result["predicted_churned"] = model.predict(X)
    result["churn_score"] = model.predict_proba(X)[:, churn_column]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(args.output, index=False)
    print(f"Saved {len(result)} predictions to {args.output}")
    print("Scores are uncalibrated; this is a retrospective educational model.")


if __name__ == "__main__":
    main()
