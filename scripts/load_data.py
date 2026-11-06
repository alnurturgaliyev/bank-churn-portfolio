from pathlib import Path

import pandas as pd
from sqlalchemy import text

from db import create_db_engine

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data" / "processed"

# Match the CSV headers to our PostgreSQL column names.
COLUMN_NAMES = {
    "LocationId": "location_id",
    "Geography": "geography",
    "CustomerId": "customer_id",
    "Gender": "gender",
    "Age": "age",
    "Salary": "salary",
    "Churned": "churned",
    "AccountId": "account_id",
    "Tenure": "tenure",
    "Balance": "balance",
    "NumProducts": "num_products",
    "HasCreditCard": "has_credit_card",
    "IsActive": "is_active",
}

# Load parent tables before tables that reference them.
TABLE_ORDER = ["location", "demographic", "account"]

tables = {
    name: pd.read_csv(DATA_DIR / f"{name}.csv").rename(
        columns=COLUMN_NAMES
    )
    for name in TABLE_ORDER
}

engine = create_db_engine()

try:
    with engine.begin() as connection:
        # Stop if data already exists, preventing accidental duplicate loads.
        for name in TABLE_ORDER:
            count = connection.execute(
                text(f"SELECT COUNT(*) FROM public.{name}")
            ).scalar_one()

            if count > 0:
                raise ValueError(
                    f"Table {name} already contains data. Loading stopped."
                )

        for name in TABLE_ORDER:
            tables[name].to_sql(
                name=name,
                con=connection,
                schema="public",
                if_exists="append",
                index=False,
                chunksize=1000,
            )

    print("Data load committed successfully.")
    for name in TABLE_ORDER:
        print(f"{name}: {len(tables[name])} rows loaded")
finally:
    engine.dispose()
