## Day 1 - Data Quality Summary

# Anomalies

*01_fund_master* - looks clean, no issues. This is the main reference table with amfi_code, fund house, category, risk grade etc.

*02_nav_history* - the big one. amfi_code, date, nav. Date is a string like the others.

*03_aum_by_fund_house* - fine, same date-as-string thing.

*04_monthly_sip_inflows* - yoy_growth_pct is coming up NaN for the first several rows. Makes sense if it's the first 12 months of the dataset (can't calculate YoY without a year of prior data), but I should double check it's not missing anywhere else too.

*05_category_inflows* - clean.

*06_industry_folio_count* - clean, but this one is quarterly (Jan/Apr/Jul/Oct) instead of monthly like most of the others. Need to keep that in mind if I ever join this against monthly data.

*07_scheme_performance* - clean. Same 40 rows and same amfi_codes as fund_master, which is a good sign - should join fine later.

*08_investor_transactions* - biggest transactional file. Nothing wrong in the sample I can see, but haven't checked yet for duplicate transactions, weird values in amount_inr, or inconsistent category labels (kyc_status, transaction_type, payment_mode). Want to run value_counts() on those columns before trusting them.

*09_portfolio_holdings* - clean, date as string again.

*10_benchmark_indices* - the head only shows NIFTY50, need to check unique() on index_name to see if there are other benchmarks in there too or if it's just the one.


# Not sure about
- yoy_growth_pct nulls - confirm limited to early rows only
- value_counts() on kyc_status, transaction_type, payment_mode in investor_transactions
- unique() on index_name in benchmark_indices
- Later: confirm every amfi_code in fund_master also shows up in nav_history

Validated that all 40 amfi_codes in fund_master exist in nav_history — no missing matches. Fund master covers 10 fund houses, 2 top-level categories (Equity/Debt), 12 sub-categories, and 5 risk categories. AMFI codes are plain integer IDs with no embedded structure — just unique identifiers, so matching across files has to be done by exact code, not by parsing the code itself.