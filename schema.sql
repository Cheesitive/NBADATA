PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS player_game_stats_pct;
DROP TABLE IF EXISTS player_game_stats;
DROP TABLE IF EXISTS games;
DROP TABLE IF EXISTS players;
DROP TABLE IF EXISTS teams;


CREATE TABLE teams (
    team_id TEXT PRIMARY KEY,
    team_name TEXT
);

CREATE TABLE players (
    player_id INTEGER PRIMARY KEY,
    player_name TEXT NOT NULL UNIQUE
);

CREATE TABLE games(
    game_id INTEGER PRIMARY KEY,
    game_date TEXT NOT NULL,
    home_team_id TEXT NOT NULL REFERENCES teams(team_id),
    away_team_id TEXT NOT NULL REFERENCES teams(team_id),
    CHECK (home_team_id <> away_team_id),
    UNIQUE (game_date, home_team_id, away_team_id)
);

CREATE TABLE player_game_stats (
    player_id INTEGER NOT NULL REFERENCES players (player_id),
    game_id INTEGER NOT NULL REFERENCES games(game_id),
    team_id TEXT NOT NULL REFERENCES teams(team_id),
    is_home INTEGER NOT NULL CHECK (is_home IN(0, 1)),
    result TEXT NOT NULL CHECK (result IN("W", "L")),
    minutes_played REAL,
    fg INTEGER NOT NULL, fga INTEGER NOT NULL,
    fg3 INTEGER NOT NULL, fg3a INTEGER NOT NULL,
    ft INTEGER NOT NULL, fta INTEGER NOT NULL,
    orb INTEGER NOT NULL, drb INTEGER NOT NULL, trb INTEGER NOT NULL,
    ast INTEGER NOT NULL, stl INTEGER NOT NULL, blk INTEGER NOT NULL,
    tov INTEGER NOT NULL, pf INTEGER NOT NULL, pts INTEGER NOT NULL,
    plus_minus INTEGER,
    game_score REAL,
    PRIMARY KEY (player_id, game_id),
    CHECK(fg <= fga AND fg3 <= fg3a AND ft <= fta AND fg3 <= fg)
);

CREATE VIEW player_game_stats_pct AS
SELECT *,
    CASE WHEN fga  > 0 THEN ROUND(1.0 * fg  / fga,  3) END AS fg_pct,
    CASE WHEN fg3a > 0 THEN ROUND(1.0 * fg3 / fg3a, 3) END AS fg3_pct,
    CASE WHEN fta  > 0 THEN ROUND(1.0 * ft  / fta,  3) END AS ft_pct
FROM player_game_stats;