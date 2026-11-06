
import pandas as pd
from scipy.stats import f_oneway
from sqlalchemy import text

from db import create_db_engine

engine = create_db_engine()

try:
    with engine.connect() as connection:
        df = pd.read_sql(
            text("""
                SELECT l.geography, a.tenure
                FROM public.demographic d
                JOIN public.account a
                    ON a.customer_id = d.customer_id
                JOIN public.location l
                    ON l.location_id = d.location_id
            """),
            connection,
        )
finally:
    engine.dispose()

summary = (
    df.groupby("geography")["tenure"]
    .agg(["count", "mean", "std", "min", "max"])
)

print("\nTenure by country:")
print(summary.round(3))
print("\nCustomers included:", len(df))

# Create one array of tenure values per country.
groups = [
    group["tenure"].to_numpy()
    for _, group in df.groupby("geography")
]

result = f_oneway(*groups, equal_var=False)

print(f"\nWelch ANOVA F-statistic: {result.statistic:.4f}")
print(f"P-value: {result.pvalue:.4e}")
print(
    "Largest observed difference between country means: "
    f"{summary['mean'].max() - summary['mean'].min():.4f}"
)
