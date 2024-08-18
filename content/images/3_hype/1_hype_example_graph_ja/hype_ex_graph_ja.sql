SELECT
    c_year AS year,
    name,
    c_pos AS position,
    adp_pos_rank AS draft_rank,
    ROUND(exp_fppg_ppr,0) AS expected_ppg,
    ROUND(prior_fppg_ppr,0) AS prior_year_ppg,
    ROUND(pick_hype,0) AS pick_hype,
    actual_pos_fin_fppg_ppr AS actual_rank,
    ROUND(fppg_ppr,0) AS actual_ppg,
    ROUND(pick_accuracy,0) AS pick_accuracy
FROM nfl_adp_hype
WHERE 1=1
    AND name LIKE 'josh allen'
    AND year != '2016'
ORDER BY c_year ASC