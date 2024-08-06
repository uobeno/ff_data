SELECT
    c_year AS year,
    c_pos AS position,
    adp_pos_rank AS draft_rank,
    exp_fppg_ppr AS expected_ppg,
    fppg_ppr AS actual_ppg,
    pick_accuracy,
    ABS(pick_accuracy) AS abs_pick_accuracy,
    IIF(pick_accuracy > 0, exp_fppg_ppr, fppg_ppr) AS bar_start,
    IIF(pick_accuracy > 0, fppg_ppr, exp_fppg_ppr) AS bar_end,
    IIF(pick_accuracy > 0, 'lightgreen', 'lightcoral') AS bar_color
FROM nfl_adp_hype
WHERE 1=1
    AND c_pos IN ("QB", "WR", "RB", "TE")
    AND name LIKE 'antonio brown'
ORDER BY c_year ASC
LIMIT 10
;