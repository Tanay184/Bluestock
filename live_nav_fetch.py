import requests
import pandas as pd
from pathlib import Path

RAW_DIR = Path("data/raw")

def fetch_scheme_nav(scheme_code: int) -> dict:
    url = f"https://api.mfapi.in/mf/{scheme_code}"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return resp.json()

def save_raw_json_as_csv(data: dict, scheme_code: int) -> Path:
    nav_df = pd.DataFrame(data["data"])
    nav_df["scheme_code"] = scheme_code
    nav_df["scheme_name"] = data["meta"]["scheme_name"]
    nav_df["fund_house"] = data["meta"]["fund_house"]

    out_path = RAW_DIR / f"live_nav_{scheme_code}.csv"
    nav_df.to_csv(out_path, index=False)
    print(f"Saved {len(nav_df)} rows -> {out_path}")
    return out_path

KEY_SCHEMES = {
    "HDFC Top 100": 125497,
    "SBI Bluechip": 119551,
    "ICICI Bluechip": 120503,
    "Nippon Large Cap": 118632,
    "Axis Bluechip": 119092,
    "Kotak Bluechip": 120841,
}

if __name__ == "__main__":
    for name, code in KEY_SCHEMES.items():
        print(f"Fetching {name} ({code})...")
        data = fetch_scheme_nav(code)
        save_raw_json_as_csv(data, code)