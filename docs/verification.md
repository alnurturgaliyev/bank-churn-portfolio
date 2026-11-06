# Verification record

Verified for the portfolio packaging on 2026-11-07. Existing PostgreSQL data and final model choices were preserved.

## Completed checks

- `python -m pip check`: no broken requirements.
- `python -m compileall -q scripts`: all scripts compile.
- `python scripts/download_data.py`: existing workbook matches the pinned SHA-256.
- `python scripts/verify_artifacts.py`: split sizes, unique/disjoint IDs, 3,617 missing balances, prediction alignment, six saved test metrics, confusion matrix, and saved-model prediction replay passed.
- `python scripts/predict.py examples/customer_example.csv --output reports/example_predictions.csv`: two synthetic example records scored successfully, including a missing balance.
- Shared database configuration was checked using environment overrides without making a database connection. Existing defaults remain localhost:5432, database bank_churn, user postgres.
- Git staging excludes the virtual environment, source and derived customer data, row-level inspection/predictions, credentials, and fitted model binary.

## Clean-file-tree reproduction

Using a separate working directory and the project's existing locked Python environment, ran:

```bash
python scripts/prepare_data.py
python scripts/prepare_model_data.py --from-csv
python scripts/evaluate_final_model.py
python scripts/verify_artifacts.py
```

The clean run used a copy of the checksum-verified workbook and the selected parameter JSON. The regenerated train.csv and test.csv were byte-identical to the original PostgreSQL-derived split files. It reproduced the saved final confusion matrix (TN 1321, FP 272, FN 102, TP 305) and six reported metrics. This was a reproducibility check with fixed settings, not a new tuning experiment.

This check did not create a fresh package environment or recreate the PostgreSQL server. The original database loading and SQL row-count/join verification were performed earlier in the workflow. Tableau remains deferred.
