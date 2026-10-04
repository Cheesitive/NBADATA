import os
import sqlite3
import pandas as pd

DB_PATH = "nba.db"
EXPORT_DIR = "exports"
TABLES = ["teams", "players", "games", "player_game_stats"]

os.makedirs(EXPORT_DIR, exist_ok=True)

with sqlite3.connect(DB_PATH) as con:
    for table in TABLES:
        df = pd.read_sql(f"SELECT * FROM {table}", con)
        out_path = os.path.join(EXPORT_DIR, f"{table}.csv")
        df.to_csv(out_path, index=False)
        print(f"Exported {len(df)} rows to {out_path}")
