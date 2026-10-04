import sqlite3

con = sqlite3.connect("nba.db")
cur = con.cursor()
cur.execute(open("queris.sql").read())
cols = [d[0] for d in cur.description]
print(" | ".join(cols))
for row in cur.fetchall():
    print(row)
