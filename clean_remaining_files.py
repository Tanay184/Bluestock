import pandas as pd
from pathlib import Path

RAW_DIR = Path("data/raw")
OUT_DIR = Path("data/processed")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Files not covered by the detailed Day 2 cleaning tasks — generic pass only
FILES = [
    "01_fund_master.csv",
    "03_aum_by_fund_house.csv",
    "04_monthly_sip_inflows.csv",
    "05_category_inflows.csv",
    "06_industry_folio_count.csv",
    "09_portfolio_holdings.csv",
    "10_benchmark_indices.csv",
]

def clean_file(filename: str):
    path = RAW_DIR / filename
    df = pd.read_csv(path)
    print(f"\n{'='*60}\n{filename}\n{'='*60}")
    print(f"Before: {df.shape}")

    # Parse any column that looks like a date
    date_cols = [c for c in df.columns if "date" in c.lower() or c.lower() == "month"]
    for col in date_cols:
        try:
            df[col] = pd.to_datetime(df[col], errors="coerce")
            bad = df[col].isnull().sum()
            if bad > 0:
                print(f"  '{col}': {bad} unparseable date values")
        except Exception as e:
            print(f"  Could not parse '{col}' as date: {e}")

    # Remove exact duplicate rows
    before = len(df)
    df = df.drop_duplicates()
    removed = before - len(df)
    if removed > 0:
        print(f"  Removed {removed} exact duplicate rows")

    # Flag negative values in numeric columns (informational only — not auto-removed)
    numeric_cols = df.select_dtypes(include="number").columns
    for col in numeric_cols:
        neg_count = (df[col] < 0).sum()
        if neg_count > 0:
            print(f"  '{col}': {neg_count} negative values — review manually")

    # Check for nulls
    null_counts = df.isnull().sum()
    nulls_found = null_counts[null_counts > 0]
    if len(nulls_found) > 0:
        print(f"  Null values found:\n{nulls_found}")

    print(f"After: {df.shape}")

    out_name = filename.replace(".csv", "_clean.csv")
    out_path = OUT_DIR / out_name
    df.to_csv(out_path, index=False)
    print(f"Saved -> {out_path}")

if __name__ == "__main__":
    for f in FILES:
        clean_file(f)
    print("\nAll 7 files processed.")
