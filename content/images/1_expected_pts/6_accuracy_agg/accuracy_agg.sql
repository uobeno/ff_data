SELECT
    c_year AS year,
    c_pos AS position,
    CASE
        WHEN adp_pos_rank <= 3 THEN '1-3'
        WHEN adp_pos_rank <= 10 THEN '4-10'
        ELSE
            CAST((((adp_pos_rank - 1) / 10) * 10 + 1) AS VARCHAR)
            || '-' ||
            CAST((((adp_pos_rank - 1) / 10) * 10 + 10) AS VARCHAR)
        END AS adp_bucket,
    MIN(adp_pos_rank) AS draft_rank,
    COUNT(1) AS player_cnt,
    ROUND(AVG(exp_fppg_ppr),2) AS expected_ppg,
    ROUND(AVG(fppg_ppr),2) AS avg_actual_ppr,
    ROUND(AVG(pick_accuracy),2) AS avg_accuracy,
    MAX(pick_accuracy) AS biggest_surprise,
    MIN(pick_accuracy) AS worst_miss
FROM nfl_adp_hype
WHERE 1=1
    AND fppg_ppr IS NOT NULL
    AND adp_pos_rank IS NOT NULL
    AND exp_fppg_ppr IS NOT NULL
GROUP BY 1, 2, 3
ORDER BY CAST(c_year AS INT) ASC, c_pos ASC, 4 ASC