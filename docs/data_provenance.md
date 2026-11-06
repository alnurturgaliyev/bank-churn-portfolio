# Source and attribution

This is a guided portfolio implementation adapted from Mehrdad Dehghan's [End-to-End Banking Customer Churn Analytics & Predictive Modeling tutorial](https://www.youtube.com/watch?v=8sfXdtYft74) and [source repository](https://github.com/M3hrdad-Dehghan/end-to-end-real-world-data-projects).

The project was built while following the tutorial with AI assistance for setup, code, debugging, and documentation. Attribution does not imply endorsement by the tutorial author.

## Dataset source

- Repository revision: `42d401a112a1f8033dfe3567ad60c744ab202f8b`.
- Workbook: `End-to-End Banking Customer Churn Analytics & Predictive Modeling/data/raw/raw_data.xlsx`.
- SHA-256: `82ebf9b30a647f65a6b8b5016da2675e4c5a6e1d4a6de2849ba8d625691bc619`.
- Sheets: Demographic (10,000 rows), Account (10,000 rows), Location (6 rows).

`python scripts/download_data.py` retrieves that exact workbook and verifies its checksum. The original workbook, derived customer data, row-level test predictions, and fitted binary are excluded from Git. They are regenerated locally; aggregate results and synthetic inference examples are included.

No license for the banking project was identified at this revision. This repository does not assign a license to the upstream materials or redistribute the workbook. Consult the source author about reuse rights. A license found in a different project directory is not treated as a license for this dataset.

## Adaptations implemented here

- PostgreSQL schema, foreign keys, and Python connections in place of SQL Server and Windows-specific setup.
- Missing balances preserved, analyzed, and imputed only inside model-training pipelines.
- Stratified split with customer-overlap checks and a dummy benchmark.
- Common validation folds for logistic regression and random forest; bounded eight-configuration forest search.
- Welch's t-test and Welch's ANOVA, with scope and interpretation limits recorded.
- Fixed-configuration final evaluation, saved pipeline, and reusable CSV scoring command.

SVM, XGBoost, the tutorial's full feature-engineering experiments, and Tableau are not implemented in this version.
