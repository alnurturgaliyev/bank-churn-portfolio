# Exploratory Analysis Findings

## Dataset and validation

- 10,000 customers, 10,000 account records, and 6 locations.
- Customer and location references passed validation.
- Joining all three tables preserved 10,000 customer rows.
- Overall churn: 2,037 customers (20.37%).
- Balance is missing for 3,617 customers (36.17%).
- Missing balances were preserved rather than assumed to be zero.

## Observed patterns

- Gender: female churn was 25.07%; male churn was 16.46%.
- Geography: country churn rates ranged from 19.37% to 21.13%.
- Age: customers over 50 had the highest churn rate within
  every country, ranging from 40.74% to 49.27%.
- Activity: inactive customers had 26.85% churn versus
  14.27% for active customers.
- Balance availability: customers with recorded balances had
  24.08% churn versus 13.82% for those with missing balances.
- Products: churn rates for 1, 2, 3, and 4 products were
  27.71%, 7.58%, 82.71%, and 100%, respectively.
  The last two groups contained only 266 and 60 customers.

## Interpretation limits

- These are descriptive associations, not causal conclusions.
- Activity status and churn were tested for independence;
  see statistical_findings.md. Other comparisons remain descriptive.
- The reason for missing balances remains unverified.
- Feature timing must be checked before predictive modeling:
  predictors should be available before the churn outcome.
- Model performance must be evaluated on held-out data;
  these exploratory findings are not evidence of predictive accuracy.
