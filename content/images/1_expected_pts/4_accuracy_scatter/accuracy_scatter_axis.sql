SELECT
    c_pos AS position,
    MIN(exp_fppg_ppr) AS min_x,
    MAX(exp_fppg_ppr) AS max_x,
    MIN(fppg_ppr) AS min_y,
    MAX(fppg_ppr) AS max_y
FROM nfl_adp_hype
WHERE 1=1
    AND c_pos IN ("QB", "WR", "RB", "TE")
    AND fppg_ppr IS NOT NULL
    AND exp_fppg_ppr IS NOT NULL
GROUP BY 1