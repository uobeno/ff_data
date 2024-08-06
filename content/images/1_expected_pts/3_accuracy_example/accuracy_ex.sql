SELECT
    c_year AS year,
    name,
    c_pos AS position,
    adp_pos_rank AS draft_rank,
    exp_fppg_ppr AS expected_ppg,
    actual_pos_fin_fppg_ppr AS actual_rank,
    fppg_ppr AS actual_ppg,
    pick_accuracy
FROM nfl_adp_hype
WHERE name LIKE 'antonio brown'
ORDER BY c_year ASC