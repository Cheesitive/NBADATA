import sqlite3


def main():
    con = sqlite3.connect("nba.db")
    cur = con.cursor()
    cur.execute(open("queris.sql", encoding="utf-8").read())
    cols = [d[0] for d in cur.description]
    print(" | ".join(cols))
    for row in cur.fetchall():
        print(row)


if __name__ == "__main__":
    main()
