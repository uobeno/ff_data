SELECT
    year,
    fantasy_pos,
    COUNT(1) AS player_cnt
FROM nfl_results
GROUP BY 1, 2
ORDER BY 1, 2
;