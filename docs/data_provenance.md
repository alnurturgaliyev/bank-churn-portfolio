# Dataset source

- Source repository: https://github.com/M3hrdad-Dehghan/end-to-end-real-world-data-projects.

- Repository revision: `42d401a112a1f8033dfe3567ad60c744ab202f8b`.
- Workbook: `End-to-End Banking Customer Churn Analytics & Predictive Modeling/data/raw/raw_data.xlsx`.
- SHA-256: `82ebf9b30a647f65a6b8b5016da2675e4c5a6e1d4a6de2849ba8d625691bc619`.
- Sheets: Demographic (10,000 rows), Account (10,000 rows), Location (6 rows).

`python scripts/download_data.py` retrieves that exact workbook and verifies its checksum. The original workbook, derived customer data, row-level test predictions, and fitted binary are excluded from Git. They are regenerated locally; aggregate results and synthetic inference examples are included.

## Implementation details

- PostgreSQL schema, foreign keys, and configurable Python connections.
- Missing balances preserved, analyzed, and imputed only inside model-training pipelines.
- Stratified split with customer-overlap checks and a dummy benchmark.
- Common validation folds for logistic regression and random forest; bounded eight-configuration forest search.
- Welch's t-test and Welch's ANOVA, with scope and interpretation limits recorded.
- Fixed-configuration final evaluation, saved pipeline, and reusable CSV scoring command.

Tableau is planned for a later version. SVM and XGBoost are not implemented in this version.
