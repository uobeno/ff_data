SELECT
    year,
    COUNT(1) AS player_cnt
FROM nfl_results
GROUP BY 1
ORDER BY 1
;