SELECT
    c_year AS year,
    c_pos AS position,
    name,
    adp_pos_rank AS draft_rank,
    fppg_ppr AS actual_points,
    exp_fppg_ppr AS expected_points
FROM nfl_adp_hype
WHERE 1=1
    AND c_pos IN ("QB", "WR", "RB", "TE")
    AND fppg_ppr IS NOT NULL
    AND exp_fppg_ppr IS NOT NULL
-- pick_accuracy