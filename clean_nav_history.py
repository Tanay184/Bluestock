import pandas as pd
from pathlib import Path

RAW_PATH = Path("data/raw/02_nav_history.csv")
OUT_PATH = Path("data/processed/02_nav_history_clean.csv")

df = pd.read_csv(RAW_PATH)
print("Before cleaning:", df.shape)

# 1. Parse dates
df["date"] = pd.to_datetime(df["date"])

# 2. Sort by amfi_code, then date
df = df.sort_values(["amfi_code", "date"]).reset_index(drop=True)

# 3. Forward-fill missing NAV per fund (holidays/weekends)
df["nav"] = df.groupby("amfi_code")["nav"].ffill()

# 4. Remove duplicate (amfi_code, date) rows
before_dupes = len(df)
df = df.drop_duplicates(subset=["amfi_code", "date"])
print(f"Removed {before_dupes - len(df)} duplicate rows")

# 5. Validate NAV > 0
invalid = df[df["nav"] <= 0]
print(f"Rows with NAV <= 0: {len(invalid)}")
if len(invalid) > 0:
    print(invalid)

print("After cleaning:", df.shape)

# Save
OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUT_PATH, index=False)
print(f"Saved -> {OUT_PATH}")