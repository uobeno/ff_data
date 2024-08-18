SELECT
    c_year AS year,
    name,
    c_pos AS position,
    adp_pos_rank AS draft_rank,
    exp_fppg_ppr AS expected_ppg,
    prior_fppg_ppr AS prior_year_ppg,
    pick_hype,
    actual_pos_fin_fppg_ppr AS actual_rank,
    fppg_ppr AS actual_ppg,
    pick_accuracy
FROM nfl_adp_hype
WHERE 1=1
    AND name LIKE 'antonio brown'
    AND year != '2016'
ORDER BY c_year ASC