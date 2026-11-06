import argparse
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split
from sqlalchemy import text

from db import create_db_engine

BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = BASE_DIR / "data" / "modeling"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

parser = argparse.ArgumentParser(description="Create the fixed stratified model split.")
parser.add_argument("--from-csv", action="store_true", help="Use processed CSVs instead of PostgreSQL")
args = parser.parse_args()

if args.from_csv:
    source = BASE_DIR / "data" / "processed"
    demographic = pd.read_csv(source / "demographic.csv")
    account = pd.read_csv(source / "account.csv")
    location = pd.read_csv(source / "location.csv")
    df = demographic.merge(account, on="CustomerId", validate="one_to_one").merge(
        location, on="LocationId", validate="many_to_one"
    )
    if len(df) != len(demographic):
        raise ValueError("Join lost customer rows.")
    df = df.rename(columns={
        "CustomerId": "customer_id", "Gender": "gender", "Age": "age",
        "Salary": "salary", "Geography": "geography", "Tenure": "tenure",
        "Balance": "balance", "NumProducts": "num_products",
        "HasCreditCard": "has_credit_card", "IsActive": "is_active", "Churned": "churned",
    })[["customer_id", "gender", "age", "salary", "geography", "tenure", "balance",
        "num_products", "has_credit_card", "is_active", "churned"]]
    df = df.sort_values("customer_id").reset_index(drop=True)
else:
    engine = create_db_engine()
    try:
        with engine.connect() as connection:
            df = pd.read_sql(
                text("""
                    SELECT
                        d.customer_id, d.gender, d.age, d.salary, l.geography,
                        a.tenure, a.balance, a.num_products, a.has_credit_card,
                        a.is_active, d.churned
                    FROM public.demographic d
                    JOIN public.account a ON a.customer_id = d.customer_id
                    JOIN public.location l ON l.location_id = d.location_id
                    ORDER BY d.customer_id
                """),
                connection,
            )
    finally:
        engine.dispose()

assert df["customer_id"].is_unique, "Customer IDs must be unique."

train, test = train_test_split(
    df,
    test_size=0.20,
    random_state=42,
    stratify=df["churned"],
)

overlap = set(train["customer_id"]) & set(test["customer_id"])
assert not overlap, "A customer appears in both splits."

train.to_csv(OUTPUT_DIR / "train.csv", index=False)
test.to_csv(OUTPUT_DIR / "test.csv", index=False)

print("Training rows:", len(train))
print("Test rows:", len(test))
print("Customers appearing in both:", len(overlap))

print("\nTraining churn counts:")
print(train["churned"].value_counts().sort_index())

print("\nSplit files saved in data/modeling/")
print("Missing balances preserved; no preprocessing fitted yet.")
