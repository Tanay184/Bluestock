"""
Simple Fund Recommender
Bluestock MF Analytics - Day 5
Input: risk appetite (Low / Moderate / High)
Output: Top 3 funds by Sharpe ratio within matching risk grade
"""

import pandas as pd
import sqlite3
import os

# --- Paths (assumes this script sits in project root) ---
DB_PATH = "bluestock_mf.db"
SCORECARD_PATH = "fund_scorecard.csv"

# --- Risk appetite mapping to actual risk_category values in the data ---
RISK_MAP = {
    "low": ["Low"],
    "moderate": ["Moderate", "Moderately High"],
    "high": ["High", "Very High"],
}

def load_data():
    conn = sqlite3.connect(DB_PATH)
    fund_df = pd.read_sql("SELECT amfi_code, scheme_name, fund_house, category, risk_category FROM dim_fund", conn)
    conn.close()

    scorecard_df = pd.read_csv(SCORECARD_PATH)
    scorecard_df["amfi_code"] = scorecard_df["amfi_code"].astype(fund_df["amfi_code"].dtype)

    merged = fund_df.merge(scorecard_df[["amfi_code", "sharpe_ratio"]], on="amfi_code", how="inner")
    return merged

def recommend_funds(risk_appetite: str, data: pd.DataFrame, top_n: int = 3) -> pd.DataFrame:
    risk_key = risk_appetite.strip().lower()
    if risk_key not in RISK_MAP:
        raise ValueError(f"Invalid risk appetite '{risk_appetite}'. Choose Low, Moderate, or High.")

    matched_categories = RISK_MAP[risk_key]
    filtered = data[data["risk_category"].isin(matched_categories)]
    top_funds = filtered.sort_values("sharpe_ratio", ascending=False).head(top_n)
    return top_funds[["amfi_code", "scheme_name", "fund_house", "category", "risk_category", "sharpe_ratio"]]

def main():
    data = load_data()
    print("=== Simple Fund Recommender ===")
    risk_input = input("Enter your risk appetite (Low / Moderate / High): ")

    try:
        recommendations = recommend_funds(risk_input, data)
        print(f"\nTop {len(recommendations)} funds for '{risk_input}' risk appetite:\n")
        print(recommendations.to_string(index=False))
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()