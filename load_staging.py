import sqlite3
import pandas as pd

CSV_PATH = "nba_dailyleaders_full_24_25.csv"
DB_PATH = "nba.db"

def parse_minutes(mp):
    if pd.isna(mp):
        return None
    parts = str(mp).split(":")
    minutes, seconds = int(parts[0]), int(parts[1])
    return round(minutes + seconds / 60, 2)

df = pd.read_csv(CSV_PATH, encoding="utf-8")
# 1. Rename columns to SQL-friendly names
df = df.rename(columns={
    "Player": "player_name", "Tm": "team", "Unnamed: 3": "away_flag",
    "Opp": "opp", "Result": "result", "MP": "mp_raw",
    "FG": "fg", "FGA": "fga", "3P": "fg3", "3PA": "fg3a", "FT": "ft", "FTA": "fta",
    "ORB": "orb", "DRB": "drb", "TRB": "trb", "AST": "ast", "STL": "stl",
    "BLK": "blk", "TOV": "tov", "PF": "pf", "PTS": "pts",
    "+/-": "plus_minus", "GmSc": "game_score", "Date": "date_raw",
})
 
# 2. US dates (10/22/2024) -> ISO dates (2024-10-22)
dates = pd.to_datetime(df["date_raw"], format="%m/%d/%Y")
df["game_date"] = dates.dt.strftime("%Y-%m-%d")
 
# 3. '@' means the player's team was away
df["is_home"] = (df["away_flag"] != "@").astype(int)
 
# 4. Minutes text -> decimal number
df["minutes_played"] = df["mp_raw"].apply(parse_minutes)
 
# 5. Keep plus/minus as a whole number even though it has NULLs
df["plus_minus"] = df["plus_minus"].astype("Int64")
 
# 6. Drop columns we can recompute or no longer need
df = df.drop(columns=["FG%", "3P%", "FT%", "away_flag"])
 
with sqlite3.connect(DB_PATH) as conn:
    df.to_sql("staging_box_scores", conn, if_exists="replace", index=False)
    n = conn.execute("SELECT COUNT(*) FROM staging_box_scores").fetchone()[0]
print(f"Loaded {n} rows into staging_box_scores")
