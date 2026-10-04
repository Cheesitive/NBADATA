"""Runs sanity checks against nba.db and prints PASS/FAIL for each.""" 

import sqlite3 

  

CHECKS = [ 

    ("Box-score rows match CSV", 

     """SELECT (SELECT COUNT(*) FROM player_game_stats) 

             = (SELECT COUNT(*) FROM staging_box_scores)"""), 

    ("Total points match CSV", 

     """SELECT (SELECT SUM(pts) FROM player_game_stats) 

             = (SELECT SUM(pts) FROM staging_box_scores)"""), 

    ("Exactly 30 teams", 

     "SELECT COUNT(*) = 30 FROM teams"), 

    ("Every game has exactly 2 teams", 

     """SELECT COUNT(*) = 0 FROM ( 

            SELECT game_id FROM player_game_stats 

            GROUP BY game_id HAVING COUNT(DISTINCT team_id) <> 2)"""), 

    ("Every game has one winner and one loser", 

     """SELECT COUNT(*) = 0 FROM ( 

            SELECT game_id FROM player_game_stats 

            GROUP BY game_id HAVING COUNT(DISTINCT result) <> 2)"""), 

    ("Every game has box-score rows", 

     """SELECT COUNT(*) = 0 FROM games g 

        WHERE NOT EXISTS ( 

            SELECT 1 FROM player_game_stats s WHERE s.game_id = g.game_id)"""), 

    ("No missing minutes", 

     "SELECT COUNT(*) = 0 FROM player_game_stats WHERE minutes_played IS NULL"), 

] 

  

with sqlite3.connect("nba.db") as conn: 

    for name, sql in CHECKS: 

        ok = conn.execute(sql).fetchone()[0] == 1 

        print(f"[{'PASS' if ok else 'FAIL'}] {name}") 

  

    orphans = conn.execute("PRAGMA foreign_key_check").fetchall() 

    status = "PASS" if not orphans else "FAIL" 

    print(f"[{status}] No broken foreign keys ({len(orphans)} found)") 