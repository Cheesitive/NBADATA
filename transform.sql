--move data from staging_box_score into normalized tables 
PRAGMA foreign_keys = ON;
BEGIN TRANSACTION;

--Step A: Unionize, remove duplicates
INSERT INTO teams (team_id)
SELECT team from staging_box_scores
UNION
SELECT opp  FROM staging_box_scores;

INSERT INTO players (player_name)
SELECT DISTINCT player_name
FROM staging_box_scores
ORDER BY player_name;

INSERT INTO games (game_date, home_team_id, away_team_id)
SELECT DISTINCT game_date, team, opp
FROM staging_box_scores
WHERE is_home = 1
ORDER BY game_date, team;

--Step D: box scores, joins translate names/teams/dates into new ID.
INSERT INTO player_game_stats (
    player_id, game_id, team_id, is_home, result, minutes_played,
    fg, fga, fg3, fg3a, ft, fta, orb, drb, trb, ast, stl, blk, tov, pf, pts,
    plus_minus, game_score
)
SELECT
    p.player_id, g.game_id, s.team, s.is_home, s.result, s.minutes_played,
    s.fg, s.fga, s.fg3, s.fg3a, s.ft, s.fta, s.orb, s.drb, s.trb,
    s.ast, s.stl, s.blk, s.tov, s.pf, s.pts,
    s.plus_minus, s.game_score
FROM staging_box_scores AS s
JOIN players AS p
    ON p.player_name = s.player_name
JOIN games AS g
    ON  g.game_date    = s.game_date
    AND g.home_team_id = CASE WHEN s.is_home = 1 THEN s.team ELSE s.opp  END
    AND g.away_team_id = CASE WHEN s.is_home = 1 THEN s.opp  ELSE s.team END;
 
COMMIT;

