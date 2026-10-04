-- Example: top 10 highest-scoring individual game performances
SELECT
    player_name,
    game_date,
    team,
    opp,
    pts,
    trb,
    ast,
    result
FROM staging_box_scores
ORDER BY pts DESC
LIMIT 10;
