import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("sqlite:///bluestock_mf.db")

def load_and_verify(csv_path, table_name, if_exists="append"):
    df = pd.read_csv(csv_path)
    df.to_sql(table_name, engine, if_exists=if_exists, index=False)
    row_count = pd.read_sql(f"SELECT COUNT(*) as cnt FROM {table_name}", engine).iloc[0]["cnt"]
    print(f"{table_name}: loaded {len(df)} rows from CSV, table now has {row_count} rows")

# dim_fund from fund_master (rename columns to match schema)
fund_master = pd.read_csv("data/raw/01_fund_master.csv")
dim_fund = fund_master[["amfi_code", "scheme_name", "fund_house", "category", "sub_category", "plan", "risk_category"]]
dim_fund.to_sql("dim_fund", engine, if_exists="append", index=False)
print(f"dim_fund: loaded {len(dim_fund)} rows")

# fact_nav from cleaned nav_history
nav = pd.read_csv("data/processed/02_nav_history_clean.csv")
nav.to_sql("fact_nav", engine, if_exists="append", index=False)
print(f"fact_nav: loaded {len(nav)} rows")

# fact_transactions from cleaned investor_transactions (rename transaction_date -> date)
txns = pd.read_csv("data/processed/08_investor_transactions_clean.csv")
txns = txns.rename(columns={"transaction_date": "date"})
txns = txns.drop(columns=["annual_income_lakh", "age_group", "gender", "city_tier"], errors="ignore")
txns.to_sql("fact_transactions", engine, if_exists="append", index=False)
print(f"fact_transactions: loaded {len(txns)} rows")

# fact_performance from cleaned scheme_performance
perf = pd.read_csv("data/processed/07_scheme_performance_clean.csv")
perf_cols = ["amfi_code", "return_1yr_pct", "return_3yr_pct", "return_5yr_pct", "sharpe_ratio",
             "sortino_ratio", "std_dev_ann_pct", "max_drawdown_pct", "expense_ratio_pct",
             "aum_crore", "morningstar_rating", "risk_grade"]
perf[perf_cols].to_sql("fact_performance", engine, if_exists="append", index=False)
print(f"fact_performance: loaded {len(perf)} rows")

# fact_aum from raw aum_by_fund_house
aum = pd.read_csv("data/raw/03_aum_by_fund_house.csv")
aum.to_sql("fact_aum", engine, if_exists="append", index=False)
print(f"fact_aum: loaded {len(aum)} rows")

# fact_sip_inflows from raw monthly_sip_inflows
sip = pd.read_csv("data/raw/04_monthly_sip_inflows.csv")
sip.to_sql("fact_sip_inflows", engine, if_exists="append", index=False)
print(f"fact_sip_inflows: loaded {len(sip)} rows")

print("\nAll tables loaded.")