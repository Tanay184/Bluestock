import pandas as pd
from pathlib import Path

RAW_DIR = Path("data/raw")

def load_all_csvs(raw_dir: Path) -> dict[str, pd.DataFrame]:
    dfs = {}
    for csv_path in sorted(raw_dir.glob("*.csv")):
        name = csv_path.stem
        df = pd.read_csv(csv_path)
        dfs[name] = df
        print(f"\n{'='*60}\n{name}\n{'='*60}")
        print(f"Shape: {df.shape}")
        print(f"\nDtypes:\n{df.dtypes}")
        print(f"\nHead:\n{df.head()}")
    return dfs

if __name__ == "__main__":
    datasets = load_all_csvs(RAW_DIR)