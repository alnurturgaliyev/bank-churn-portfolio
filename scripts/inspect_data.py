from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "raw" / "raw_data.xlsx"

sheets = pd.read_excel(DATA_PATH, sheet_name=None)

for sheet_name, df in sheets.items():
    print(f"\n{'=' * 60}")
    print(f"Sheet: {sheet_name}")
    print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")

    print("\nFirst 5 rows:")
    print(df.head().to_string(index=False))

    print("\nColumn types:")
    print(df.dtypes)

    print("\nMissing values per column:")
    print(df.isna().sum())

    print(f"\nFully duplicated rows: {df.duplicated().sum()}")

demographic = sheets["Demographic"]
account = sheets["Account"]
location = sheets["Location"]

print("\n--- ID checks ---")

for table_name, df, key in [
    ("Demographic", demographic, "CustomerId"),
    ("Account", account, "AccountId"),
    ("Location", location, "LocationId"),
]:
    print(f"{table_name}: repeated {key} values = {df[key].duplicated().sum()}")

print(
    "Account: repeated CustomerId values =",
    account["CustomerId"].duplicated().sum(),
)

print(
    "Account rows with unknown customers =",
    (~account["CustomerId"].isin(demographic["CustomerId"])).sum(),
)

print(
    "Customers without an account =",
    (~demographic["CustomerId"].isin(account["CustomerId"])).sum(),
)

print(
    "Customers with unknown locations =",
    (~demographic["LocationId"].isin(location["LocationId"])).sum(),
)

print("\n--- Category values ---")
print("Gender:", demographic["Gender"].unique())
print("Churned:", demographic["Churned"].unique())
print("HasCreditCard:", account["HasCreditCard"].unique())
print("IsActive:", account["IsActive"].unique())

print("\nAll locations:")
print(location.to_string(index=False))

print("\n--- Numerical ranges ---")

print("\nDemographic:")
print(demographic[["Age", "Salary"]].describe().round(2))

print("\nAccount:")
print(account[["Tenure", "Balance", "NumProducts"]].describe().round(2))

print("\n--- Balance checks ---")
print("Missing balances:", account["Balance"].isna().sum())
print("Zero balances:", account["Balance"].eq(0).sum())
print("Negative balances:", account["Balance"].lt(0).sum())

print("\n--- Churn counts ---")
print(demographic["Churned"].value_counts().sort_index())
