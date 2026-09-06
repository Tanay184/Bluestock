# Data Dictionary — Bluestock MF Capstone

Database: `bluestock_mf.db` (SQLite). Star schema with 2 dimension tables and 5 fact tables.

---

## dim_fund
Dimension table — one row per mutual fund scheme. Source: `01_fund_master.csv`.

| Column | Type | Description |
|---|---|---|
| amfi_code | INTEGER (PK) | Unique scheme identifier assigned by AMFI. Plain numeric ID, no embedded structure. |
| scheme_name | TEXT | Full name of the fund scheme, including plan type (e.g. "SBI Bluechip Fund - Regular Plan - Growth"). |
| fund_house | TEXT | Asset management company (AMC) that manages the fund. |
| category | TEXT | Top-level fund category — Equity or Debt. |
| sub_category | TEXT | More specific fund type (e.g. Large Cap, Mid Cap, Liquid, Gilt). |
| plan | TEXT | Plan variant (e.g. Regular, Direct). |
| risk_category | TEXT | SEBI-style riskometer rating (Low, Moderate, High, Very High, Moderately High). |

## dim_date
Dimension table — calendar reference. Currently unpopulated (schema defined for future use with derived year/month/quarter/day_of_week breakdowns); date fields elsewhere in the database are stored as raw ISO strings and can be joined once populated.

| Column | Type | Description |
|---|---|---|
| date | TEXT (PK) | Calendar date, ISO format (YYYY-MM-DD). |
| year | INTEGER | Calendar year. |
| month | INTEGER | Calendar month (1-12). |
| quarter | INTEGER | Calendar quarter (1-4). |
| day_of_week | TEXT | Day name (e.g. Monday). |

## fact_nav
Fact table — daily NAV per scheme. Source: `02_nav_history.csv` (cleaned → `data/processed/02_nav_history_clean.csv`).

| Column | Type | Description |
|---|---|---|
| amfi_code | INTEGER (FK → dim_fund) | Scheme identifier. |
| date | TEXT (FK → dim_date) | NAV date. |
| nav | REAL | Net Asset Value per unit on that date. |

Cleaning applied: parsed dates, sorted by amfi_code + date, forward-filled missing NAV values (holidays/weekends), removed duplicate (amfi_code, date) rows, validated nav > 0.

## fact_transactions
Fact table — individual investor transactions. Source: `08_investor_transactions.csv` (cleaned → `data/processed/08_investor_transactions_clean.csv`).

| Column | Type | Description |
|---|---|---|
| transaction_id | INTEGER (PK, autoincrement) | Unique transaction identifier (generated on load). |
| investor_id | TEXT | Identifier for the investor making the transaction. |
| amfi_code | INTEGER (FK → dim_fund) | Scheme the transaction relates to. |
| date | TEXT (FK → dim_date) | Transaction date. |
| transaction_type | TEXT | SIP, Lumpsum, or Redemption. |
| amount_inr | INTEGER | Transaction amount in INR. |
| state | TEXT | Investor's state. |
| city | TEXT | Investor's city. |
| payment_mode | TEXT | Method used for the transaction. |
| kyc_status | TEXT | Verified or Pending. |

Cleaning applied: parsed transaction dates, confirmed transaction_type and kyc_status values were already standardized (no remapping needed), validated amount_inr > 0, checked for duplicate transactions (none found).

## fact_performance
Fact table — performance and risk metrics per scheme. Source: `07_scheme_performance.csv` (cleaned → `data/processed/07_scheme_performance_clean.csv`).

| Column | Type | Description |
|---|---|---|
| amfi_code | INTEGER (PK, FK → dim_fund) | Scheme identifier. |
| return_1yr_pct | REAL | 1-year return, percent. |
| return_3yr_pct | REAL | 3-year annualized return, percent. |
| return_5yr_pct | REAL | 5-year annualized return, percent. |
| sharpe_ratio | REAL | Risk-adjusted return measure. |
| sortino_ratio | REAL | Downside-risk-adjusted return measure. |
| std_dev_ann_pct | REAL | Annualized standard deviation of returns, percent. |
| max_drawdown_pct | REAL | Maximum peak-to-trough decline, percent. |
| expense_ratio_pct | REAL | Annual fund expense ratio, percent. |
| aum_crore | INTEGER | Assets under management, in INR crore. |
| morningstar_rating | INTEGER | Morningstar star rating (1-5). |
| risk_grade | TEXT | Risk grade as reported alongside performance metrics. |

Cleaning applied: coerced all metric columns to numeric (no coercion errors found), flagged rows with negative AUM/expense ratio or extreme returns (none found), validated expense_ratio_pct falls within 0.1%-2.5% (all in range).

## fact_aum
Fact table — AUM by fund house over time. Source: `03_aum_by_fund_house.csv` (loaded as-is, no cleaning step performed today).

| Column | Type | Description |
|---|---|---|
| fund_house | TEXT | Asset management company. |
| date | TEXT (FK → dim_date) | Reporting date for the AUM snapshot. |
| aum_lakh_crore | REAL | AUM in lakh crore INR. |
| aum_crore | INTEGER | AUM in crore INR. |
| num_schemes | INTEGER | Number of schemes offered by the fund house on that date. |

## fact_sip_inflows
Fact table — industry-wide monthly SIP statistics (not scheme-specific). Source: `04_monthly_sip_inflows.csv` (loaded as-is, no cleaning step performed today).

| Column | Type | Description |
|---|---|---|
| month | TEXT (PK) | Month in YYYY-MM format. |
| sip_inflow_crore | INTEGER | Total SIP inflow for the month, in INR crore. |
| active_sip_accounts_crore | REAL | Active SIP accounts, in crore. |
| new_sip_accounts_lakh | REAL | New SIP accounts opened that month, in lakh. |
| sip_aum_lakh_crore | REAL | Total SIP AUM, in lakh crore. |
| yoy_growth_pct | REAL | Year-over-year growth in SIP inflow, percent. Null for the first 12 months of the series (no prior-year value to compare against). |

---

## Notes
- All source CSVs originally had date columns loaded as strings by pandas; dates are stored as ISO-format TEXT throughout the database.
- `dim_date` is defined in the schema but not yet populated — date values currently live only as raw strings inside the fact tables.
- `fact_aum` and `fact_sip_inflows` were loaded directly from raw data without a dedicated cleaning pass, since they weren't among the three files specified for cleaning today.
