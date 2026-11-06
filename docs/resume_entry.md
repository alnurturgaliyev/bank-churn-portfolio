# Resume entry

**Banking Customer Churn Analytics & Predictive Modeling** | Python, PostgreSQL, pandas, SciPy, scikit-learn  
[GitHub repository](https://github.com/alnurturgaliyev/bank-churn-portfolio)

- Built a Python–PostgreSQL workflow for 10,000 customer records, including relational data validation, SQL churn analysis, and exploratory statistical testing.
- Compared classification pipelines with stratified cross-validation and tuned a random forest, achieving ROC AUC 0.862 and 74.9% churn recall on a 2,000-customer test split; packaged preprocessing and inference for reuse.

## Shorter version

- Analyzed 10,000 banking customer records using Python and PostgreSQL; tuned a random forest achieving 0.862 test ROC AUC and detecting 305 of 407 churners.

## Interview explanation

This was a guided portfolio implementation based on Mehrdad Dehghan's tutorial, adapted to PostgreSQL on macOS with AI assistance. I inspected the source data, preserved missing balances, validated joins, explored churn patterns with SQL, ran statistical comparisons, and compared models using a preprocessing pipeline inside cross-validation. I selected a random forest using training-fold F1, fixed its threshold, and evaluated it on a separate test portion. Full-dataset exploration happened before the split, which I document as an evaluation limitation. Tableau is deferred. The work demonstrates retrospective analysis and modeling, not production deployment or measured retention uplift.

## Claims to avoid

Do not list a Tableau dashboard as completed, describe the tutorial data as verified real bank data, claim deployment or revenue/retention impact, or describe the model scores as calibrated customer probabilities.
