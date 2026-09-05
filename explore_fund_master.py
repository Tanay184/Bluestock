import pandas as pd

fund_master = pd.read_csv("data/raw/01_fund_master.csv")

print("Unique fund houses:", fund_master["fund_house"].nunique())
print(fund_master["fund_house"].unique())

print("\nUnique categories:")
print(fund_master["category"].unique())

print("\nUnique sub-categories:")
print(fund_master["sub_category"].unique())

print("\nUnique risk categories:")
print(fund_master["risk_category"].unique())

print("\nSample AMFI codes:")
print(fund_master["amfi_code"].head(10).tolist())
print("\nAMFI code dtype:", fund_master["amfi_code"].dtype)

nav_history = pd.read_csv("data/raw/02_nav_history.csv")

master_codes = set(fund_master["amfi_code"])
nav_codes = set(nav_history["amfi_code"])

missing = master_codes - nav_codes
print(f"\nCodes in fund_master: {len(master_codes)}")
print(f"Codes in nav_history: {len(nav_codes)}")
print(f"Codes in fund_master but MISSING from nav_history: {len(missing)}")
if missing:
    print(missing)
else:
    print("All fund_master codes found in nav_history — validation passed.")