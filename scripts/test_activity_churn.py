from math import sqrt

import pandas as pd
from scipy.stats import chi2_contingency
from sqlalchemy import text

from db import create_db_engine

engine = create_db_engine()

try:
    with engine.connect() as connection:
        df = pd.read_sql(
            text("""
                SELECT a.is_active, d.churned
                FROM public.demographic d
                JOIN public.account a
                    ON a.customer_id = d.customer_id
            """),
            connection,
        )
finally:
    engine.dispose()

# Rows: activity status. Columns: churn status.
observed = pd.crosstab(df["is_active"], df["churned"])

# Pearson's chi-square test without continuity correction.
chi2, p_value, dof, expected = chi2_contingency(
    observed,
    correction=False,
)

# Cramér's V measures the strength of the association.
n = observed.to_numpy().sum()
cramers_v = sqrt(chi2 / (n * (min(observed.shape) - 1)))

print("\nObserved counts:")
print(observed)

print("\nExpected counts if independent:")
print(
    pd.DataFrame(
        expected,
        index=observed.index,
        columns=observed.columns,
    ).round(2)
)

print(f"\nChi-square statistic: {chi2:.4f}")
print(f"Degrees of freedom: {dof}")
print(f"P-value: {p_value:.4e}")
print(f"Smallest expected count: {expected.min():.2f}")
print(f"Cramér's V: {cramers_v:.4f}")
