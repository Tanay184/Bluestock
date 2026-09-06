import pandas as pd
from pathlib import Path

RAW_PATH = Path("data/raw/07_scheme_performance.csv")
OUT_PATH = Path("data/processed/07_scheme_performance_clean.csv")

df = pd.read_csv(RAW_PATH)
print("Before cleaning:", df.shape)

# 1. Confirm all return/ratio columns are genuinely numeric (already float64, but double-check for NaNs introduced by bad values)
numeric_cols = [
    "return_1yr_pct", "return_3yr_pct", "return_5yr_pct", "benchmark_3yr_pct",
    "alpha", "beta", "sharpe_ratio", "sortino_ratio", "std_dev_ann_pct",
    "max_drawdown_pct", "aum_crore", "expense_ratio_pct"
]
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

nulls_after = df[numeric_cols].isnull().sum()
print("\nNulls introduced by numeric coercion (should be 0 if already clean):")
print(nulls_after[nulls_after > 0])

# 2. Flag anomalies — negative AUM, absurd returns, negative expense ratio
anomalies = df[(df["aum_crore"] < 0) | (df["expense_ratio_pct"] < 0) | (df["return_1yr_pct"].abs() > 200)]
print(f"\nFlagged anomaly rows: {len(anomalies)}")
if len(anomalies) > 0:
    print(anomalies[["amfi_code", "scheme_name", "aum_crore", "expense_ratio_pct", "return_1yr_pct"]])

# 3. Validate expense_ratio_pct is within 0.1% - 2.5%
out_of_range = df[(df["expense_ratio_pct"] < 0.1) | (df["expense_ratio_pct"] > 2.5)]
print(f"\nRows with expense_ratio_pct outside 0.1%-2.5%: {len(out_of_range)}")
if len(out_of_range) > 0:
    print(out_of_range[["amfi_code", "scheme_name", "expense_ratio_pct"]])

print("\nAfter cleaning:", df.shape)

OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUT_PATH, index=False)
print(f"Saved -> {OUT_PATH}")