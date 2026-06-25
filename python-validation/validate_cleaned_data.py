# validate_cleaned_data.py
# Purpose:
# Validate and prepare the ecommerce cosmetics dataset after SQL cleaning logic.

from pathlib import Path
import pandas as pd


# --------------------------------------------------
# File paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[1]

RAW_FILE = BASE_DIR / "data" / "raw" / "E-commerce cosmetic dataset.csv"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
REPORT_DIR = BASE_DIR / "docs"

CLEANED_FILE = PROCESSED_DIR / "ecommerce_cosmetics_clean.csv"
REPORT_FILE = REPORT_DIR / "data_validation_report.txt"


# --------------------------------------------------
# Load raw dataset
# --------------------------------------------------

df = pd.read_csv(RAW_FILE)

print("Raw dataset loaded successfully.")
print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")


# --------------------------------------------------
# Standardize column names
# --------------------------------------------------

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("-", "_")
)

# Rename columns for cleaner analytical names
df = df.rename(columns={
    "title_href": "title_href",
    "type": "product_type",
    "size": "product_size",
    "noofratings": "no_of_ratings"
})


# --------------------------------------------------
# Basic cleaning
# --------------------------------------------------

text_columns = [
    "product_name",
    "website",
    "country",
    "category",
    "subcategory",
    "title_href",
    "brand",
    "ingredients",
    "form",
    "product_type",
    "color",
    "product_size"
]

for col in text_columns:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip()
        df[col] = df[col].replace({"": pd.NA, "nan": pd.NA})


# --------------------------------------------------
# Numeric conversion
# --------------------------------------------------

if "price" in df.columns:
    df["price"] = (
        df["price"]
        .astype(str)
        .str.replace("$", "", regex=False)
        .str.replace("€", "", regex=False)
        .str.replace("₹", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
    )
    df["price"] = pd.to_numeric(df["price"], errors="coerce")

if "rating" in df.columns:
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")

if "no_of_ratings" in df.columns:
    df["no_of_ratings"] = (
        df["no_of_ratings"]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.strip()
    )
    df["no_of_ratings"] = pd.to_numeric(df["no_of_ratings"], errors="coerce")


# --------------------------------------------------
# Remove duplicate rows
# --------------------------------------------------

duplicate_rows = df.duplicated().sum()
df = df.drop_duplicates()


# --------------------------------------------------
# Validation checks
# --------------------------------------------------

validation_results = {}

validation_results["total_rows_after_cleaning"] = len(df)
validation_results["duplicate_rows_removed"] = int(duplicate_rows)

if "product_name" in df.columns:
    validation_results["missing_product_name"] = int(df["product_name"].isna().sum())

if "price" in df.columns:
    validation_results["missing_price"] = int(df["price"].isna().sum())
    validation_results["negative_price_count"] = int((df["price"] < 0).sum())

if "rating" in df.columns:
    validation_results["missing_rating"] = int(df["rating"].isna().sum())
    validation_results["invalid_rating_count"] = int(
        ((df["rating"] < 0) | (df["rating"] > 5)).sum()
    )

if "no_of_ratings" in df.columns:
    validation_results["missing_no_of_ratings"] = int(df["no_of_ratings"].isna().sum())
    validation_results["negative_no_of_ratings_count"] = int(
        (df["no_of_ratings"] < 0).sum()
    )


# --------------------------------------------------
# Save cleaned data and validation report
# --------------------------------------------------

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

df.to_csv(CLEANED_FILE, index=False)

with open(REPORT_FILE, "w", encoding="utf-8") as report:
    report.write("Ecommerce Cosmetics Data Validation Report\n")
    report.write("=========================================\n\n")

    for key, value in validation_results.items():
        report.write(f"{key}: {value}\n")

print("\nValidation completed successfully.")
print(f"Cleaned file saved to: {CLEANED_FILE}")
print(f"Validation report saved to: {REPORT_FILE}")
