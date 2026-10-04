import sqlite3
import subprocess
import sys

DB_PATH = "nba.db"

def run_sql_file(conn, path): 

    with open(path, encoding="utf-8") as f: 

        conn.executescript(f.read()) 

    print(f"Ran {path}") 

  

# 1. Load raw CSV into the staging table (cleaned by pandas) 

subprocess.run([sys.executable, "load_staging.py"], check=True) 

  

with sqlite3.connect(DB_PATH) as conn: 

    conn.execute("PRAGMA foreign_keys = ON") 

    # 2. (Re)create the normalized tables 

    run_sql_file(conn, "schema.sql") 

    # 3. Move data from staging into normalized tables 

    run_sql_file(conn, "transform.sql") 

    # 4. Build indexes 

    run_sql_file(conn, "indexes.sql") 

    # 5. Report row counts 

    for table in ["teams", "players", "games", "player_game_stats"]: 

        n = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0] 

        print(f"{table:<20} {n:>6} rows") 