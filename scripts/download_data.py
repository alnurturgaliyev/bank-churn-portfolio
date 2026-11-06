"""Download the tutorial workbook at a fixed source revision and verify it."""

import hashlib
from pathlib import Path
import subprocess
from urllib.parse import quote

BASE_DIR = Path(__file__).resolve().parents[1]
REVISION = "42d401a112a1f8033dfe3567ad60c744ab202f8b"
SOURCE_PATH = (
    "End-to-End Banking Customer Churn Analytics & Predictive Modeling/"
    "data/raw/raw_data.xlsx"
)
URL = (
    "https://raw.githubusercontent.com/M3hrdad-Dehghan/"
    f"end-to-end-real-world-data-projects/{REVISION}/{quote(SOURCE_PATH)}"
)
EXPECTED_SHA256 = "82ebf9b30a647f65a6b8b5016da2675e4c5a6e1d4a6de2849ba8d625691bc619"
destination = BASE_DIR / "data" / "raw" / "raw_data.xlsx"
destination.parent.mkdir(parents=True, exist_ok=True)

if not destination.exists():
    temporary = destination.with_suffix(".xlsx.download")
    try:
        subprocess.run(
            ["curl", "--fail", "--location", "--max-time", "120", URL,
             "--output", str(temporary)],
            check=True,
        )
        if hashlib.sha256(temporary.read_bytes()).hexdigest() != EXPECTED_SHA256:
            raise ValueError("Downloaded workbook checksum does not match.")
        temporary.replace(destination)
    finally:
        temporary.unlink(missing_ok=True)

if hashlib.sha256(destination.read_bytes()).hexdigest() != EXPECTED_SHA256:
    raise ValueError("Existing workbook differs from the documented source; not overwritten.")

print("Verified raw_data.xlsx SHA-256:", EXPECTED_SHA256)
