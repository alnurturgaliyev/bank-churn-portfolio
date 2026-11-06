from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "raw" / "raw_data.xlsx"
OUTPUT_DIR = BASE_DIR / "data" / "processed"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

sheets = pd.read_excel(DATA_PATH, sheet_name=None)

# Names aren't needed for our analysis or prediction.
demographic = sheets["Demographic"].drop(columns=["Name"])

# Preserve the original IDs and missing balances.
account = sheets["Account"].copy()
location = sheets["Location"].copy()

tables = {
    "demographic": demographic,
    "account": account,
    "location": location,
}

for table_name, df in tables.items():
    output_path = OUTPUT_DIR / f"{table_name}.csv"
    df.to_csv(output_path, index=False)
    print(f"Saved {output_path.name}: {len(df)} rows")

print(
    "Missing balances preserved:",
    account["Balance"].isna().sum(),
)
