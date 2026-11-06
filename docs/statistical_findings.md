# Exploratory Statistical Tests

## Activity status and churn

- Method: Pearson chi-square test without continuity correction.
- Null hypothesis: activity status and churn are independent.
- Sample: 10,000 customers, one observation per customer.
- Chi-square: 243.7604; degrees of freedom: 1.
- P-value: 5.9539e-55.
- Smallest expected count: 987.74.
- Cramér's V: 0.1561.
- Inactive churn: 26.85%; active churn: 14.27%.
- Observed difference: 12.58 percentage points.

At alpha = 0.05, reject the null hypothesis of independence,
subject to the test's assumptions. The association is modest
and does not establish causation or predictive performance.

This test was selected after exploring the same dataset.
Results are exploratory; generalization depends on how the
data was collected and whether observations are independent.

## Recorded balance and churn

- Method: two-sided Welch's independent-samples t-test.
- Null hypothesis: mean recorded balances are equal between
  churned and retained customers.
- Included: 6,383 customers with recorded balances.
- Excluded: 3,617 customers with missing balances.
- Retained: n = 4,846; mean = 119,535.86.
- Churned: n = 1,537; mean = 120,746.97.
- Mean difference (churned minus retained): 1,211.11.
- T-statistic: 1.3605; degrees of freedom: 2539.63.
- P-value: 0.1738.
- 95% confidence interval for the difference:
  [-534.50, 2956.71].

At alpha = 0.05, fail to reject the equal-means hypothesis.
This does not establish equivalence or rule out predictive value.

The analysis is exploratory and restricted to recorded balances.
Because missingness differs by churn status, these results
cannot automatically be generalized to all customers.

## Tenure across countries

- Method: Welch's one-way ANOVA.
- Null hypothesis: all six countries have equal population
  mean tenure.
- Customers included: 10,000.
- F-statistic: 0.9044.
- P-value: 0.47701.
- Highest observed mean: UK, approximately 5.127.
- Lowest observed mean: Spain, approximately 4.928.
- Largest observed mean difference: 0.1995 tenure units.

At alpha = 0.05, fail to reject the equal-means hypothesis.
This does not prove equivalence between countries.

The analysis is exploratory and assumes independent observations.
It compares tenure across countries; it does not test the
relationship between tenure and churn.
