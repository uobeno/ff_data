SELECT
    year,
    fpos,
    COUNT(1) AS player_cnt
FROM enhanced_adp
GROUP BY 1, 2
ORDER BY 1, 2
;