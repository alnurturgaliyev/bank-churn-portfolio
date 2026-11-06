
import pandas as pd
from scipy.stats import ttest_ind
from sqlalchemy import text

from db import create_db_engine

engine = create_db_engine()

try:
    with engine.connect() as connection:
        df = pd.read_sql(
            text("""
                SELECT a.balance, d.churned
                FROM public.demographic d
                JOIN public.account a
                    ON a.customer_id = d.customer_id
            """),
            connection,
        )
finally:
    engine.dispose()

print("Customers excluded for missing balance:", df["balance"].isna().sum())

# Keep only recorded balances for this test.
recorded = df.dropna(subset=["balance"])

churned = recorded.loc[recorded["churned"] == 1, "balance"]
retained = recorded.loc[recorded["churned"] == 0, "balance"]

print("\nRecorded balance summary (0 = retained, 1 = churned):")
print(
    recorded.groupby("churned")["balance"]
    .agg(["count", "mean", "std", "median"])
    .round(2)
)

result = ttest_ind(
    churned,
    retained,
    equal_var=False,
    alternative="two-sided",
)

difference = churned.mean() - retained.mean()
interval = result.confidence_interval(confidence_level=0.95)

print(f"\nMean difference (churned - retained): {difference:.2f}")
print(f"T-statistic: {result.statistic:.4f}")
print(f"Degrees of freedom: {result.df:.2f}")
print(f"P-value: {result.pvalue:.4e}")
print(
    "95% confidence interval for the mean difference: "
    f"[{interval.low:.2f}, {interval.high:.2f}]"
)
