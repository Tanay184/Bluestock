import sqlite3

conn = sqlite3.connect("bluestock_mf.db")
with open("queries.sql") as f:
    script = f.read()

queries = [q.strip() for q in script.split(";") if q.strip() and not q.strip().startswith("--")]
# Better: split by the -- N. comment markers to keep queries with their leading comment intact
import re
blocks = re.split(r"(?=-- \d+\.)", script)
for block in blocks:
    if not block.strip():
        continue
    query = block.split("\n", 1)[1] if "\n" in block else block
    label = block.split("\n")[0]
    print(f"\n{'='*60}\n{label}\n{'='*60}")
    try:
        cursor = conn.execute(query)
        rows = cursor.fetchmany(5)
        for row in rows:
            print(row)
    except Exception as e:
        print(f"ERROR: {e}")

conn.close()