from pathlib import Path
import json

ROOT = Path(r"c:\Users\Tanay\Bluestock")
NOTEBOOKS_DIR = ROOT / "notebooks"
NOTEBOOKS_DIR.mkdir(exist_ok=True)

def cell(cell_type: str, source: str | list[str]):
    if isinstance(source, str):
        source = source.splitlines(keepends=True)
    return {
        "cell_type": cell_type,
        "metadata": {},
        "source": source,
    }

def make_notebook(title: str, code_blocks: list[str]):
    cells = [
        cell("markdown", f"# {title}\n\nThis notebook was scaffolded from the project Python files.\n"),
    ]
    for block in code_blocks:
        cells.append(cell("code", block))
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "name": "python",
                "version": "3.x",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }

def file_exists(*candidates: str) -> Path | None:
    for candidate in candidates:
        path = ROOT / candidate
        if path.exists():
            return path
    return None

def load_module_snippet(module_label: str, *candidates: str) -> str:
    resolved = file_exists(*candidates)
    if resolved is None:
        return f"""
print("No matching {module_label} file found yet. Add the logic here.")
"""
    return f"""
import importlib.util
from pathlib import Path
import sys

root = Path(r"{ROOT}")
module_path = Path(r"{resolved}")

spec = importlib.util.spec_from_file_location("{module_label}_mod", module_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

print(f"Loaded: {{module_path.name}}")
print("Available functions:")
for name in [n for n in dir(module) if not n.startswith('_')]:
    print(" -", name)
"""

nb_specs = {
    "01_data_ingestion.ipynb": make_notebook(
        "01. Data Ingestion",
        [
            """
import sys
from pathlib import Path

root = Path(r"c:\\Users\\Tanay\\Bluestock")
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

from data_ingestion import load_all_csvs

raw_dir = root / "data" / "raw"
datasets = load_all_csvs(raw_dir)
print("Loaded datasets:", list(datasets.keys()))
            """,
        ],
    ),
    "02_data_cleaning.ipynb": make_notebook(
        "02. Data Cleaning",
        [
            load_module_snippet(
                "cleaning",
                "scripts/etl_pipeline.py",
                "scripts/data_cleaning.py",
                "data_cleaning.py",
            ),
        ],
    ),
    "03_eda_analysis.ipynb": make_notebook(
        "03. EDA Analysis",
        [
            load_module_snippet(
                "eda",
                "scripts/etl_pipeline.py",
                "scripts/eda_analysis.py",
                "eda_analysis.py",
            ),
        ],
    ),
    "04_performance_analytics.ipynb": make_notebook(
        "04. Performance Analytics",
        [
            load_module_snippet(
                "performance",
                "scripts/compute_metrics.py",
                "scripts/performance_analytics.py",
                "performance_analytics.py",
            ),
        ],
    ),
    "05_advanced_analytics.ipynb": make_notebook(
        "05. Advanced Analytics",
        [
            load_module_snippet(
                "advanced",
                "scripts/recommender.py",
                "scripts/advanced_analytics.py",
                "advanced_analytics.py",
            ),
        ],
    ),
}

for filename, notebook in nb_specs.items():
    path = NOTEBOOKS_DIR / filename
    with path.open("w", encoding="utf-8") as f:
        json.dump(notebook, f, ensure_ascii=False, indent=1)
    print(f"Created: {path}")