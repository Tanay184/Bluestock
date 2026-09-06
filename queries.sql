-- 1. Top 5 funds by AUM
SELECT f.scheme_name, f.fund_house, p.aum_crore
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
ORDER BY p.aum_crore DESC
LIMIT 5;

-- 2. Average NAV per month, per fund
SELECT amfi_code, strftime('%Y-%m', date) AS month, AVG(nav) AS avg_nav
FROM fact_nav
GROUP BY amfi_code, month
ORDER BY amfi_code, month;

-- 3. SIP YoY growth over time
SELECT month, sip_inflow_crore, yoy_growth_pct
FROM fact_sip_inflows
ORDER BY month;

-- 4. Transactions by state
SELECT state, COUNT(*) AS num_transactions, SUM(amount_inr) AS total_amount
FROM fact_transactions
GROUP BY state
ORDER BY total_amount DESC;

-- 5. Funds with expense ratio below 1%
SELECT f.scheme_name, p.expense_ratio_pct
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
WHERE p.expense_ratio_pct < 1.0
ORDER BY p.expense_ratio_pct;

-- 6. Top 5 funds by 3-year Sharpe ratio
SELECT f.scheme_name, p.sharpe_ratio, p.return_3yr_pct
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
ORDER BY p.sharpe_ratio DESC
LIMIT 5;

-- 7. Transaction type breakdown (count and total amount)
SELECT transaction_type, COUNT(*) AS num_transactions, SUM(amount_inr) AS total_amount
FROM fact_transactions
GROUP BY transaction_type;

-- 8. Risk category distribution across funds
SELECT risk_category, COUNT(*) AS num_funds
FROM dim_fund
GROUP BY risk_category
ORDER BY num_funds DESC;

-- 9. Monthly AUM trend by fund house
SELECT fund_house, date, aum_crore
FROM fact_aum
ORDER BY fund_house, date;

-- 10. KYC verification status breakdown by transaction type
SELECT transaction_type, kyc_status, COUNT(*) AS num_transactions
FROM fact_transactions
GROUP BY transaction_type, kyc_status;