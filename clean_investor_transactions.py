import pandas as pd
from pathlib import Path

RAW_PATH = Path("data/raw/08_investor_transactions.csv")
OUT_PATH = Path("data/processed/08_investor_transactions_clean.csv")

df = pd.read_csv(RAW_PATH)
print("Before cleaning:", df.shape)

# 1. Parse transaction_date
df["transaction_date"] = pd.to_datetime(df["transaction_date"], errors="coerce")
bad_dates = df["transaction_date"].isnull().sum()
print(f"Rows with unparseable dates: {bad_dates}")

# 2. transaction_type and kyc_status already clean (verified above) — no remapping needed

# 3. Validate amount_inr > 0
invalid_amount = df[df["amount_inr"] <= 0]
print(f"Rows with amount_inr <= 0: {len(invalid_amount)}")
if len(invalid_amount) > 0:
    print(invalid_amount[["investor_id", "transaction_type", "amount_inr"]])

# 4. Check for duplicate transactions (same investor, date, amount, type)
dupes = df.duplicated(subset=["investor_id", "transaction_date", "amfi_code", "amount_inr", "transaction_type"])
print(f"Duplicate transactions found: {dupes.sum()}")
df = df[~dupes]

print("After cleaning:", df.shape)

OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUT_PATH, index=False)
print(f"Saved -> {OUT_PATH}")