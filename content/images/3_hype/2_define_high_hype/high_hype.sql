SELECT
    c_year AS year,
    name,
    c_pos AS position,
    adp_pos_rank AS draft_rank,
    ROUND(exp_fppg_ppr,0) AS expected_ppg,
    ROUND(prior_fppg_ppr,0) AS prior_year_ppg,
    ROUND(pick_hype/exp_fppg_ppr,2) AS pick_hype,
    -- ROUND(exp_fppg_ppr,0) AS pick_hype,
    yid,
    IIF(yid=1,'Rookie', 'Non-rookie') AS rook_flag
FROM nfl_adp_hype
WHERE 1=1
    -- We're going to look at rookies
    -- But 2016 is the first year in the data
    -- So we need to ignore it to flag first year players
    AND year != '2016'
    AND pick_hype IS NOT NULL
    AND pick_hype > 2
    AND c_pos IN ("QB", "WR", "RB", "TE")