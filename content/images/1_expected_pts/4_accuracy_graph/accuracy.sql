SELECT
    c_year AS year,
    c_pos AS position,
    name,
    adp_pos_rank AS draft_rank,
    exp_fppg_ppr AS expected_ppg,
    fppg_ppr AS actual_ppg,
    actual_pos_fin_fppg_ppr AS actual_rank,
    pick_accuracy,
    ABS(pick_accuracy) AS abs_pick_accuracy,
    IIF(pick_accuracy > 0, exp_fppg_ppr, fppg_ppr) AS bar_start,
    IIF(pick_accuracy > 0, fppg_ppr, exp_fppg_ppr) AS bar_end,
    IIF(pick_accuracy > 0, 'green', 'firebrick') AS bar_color,
    MAX(exp_fppg_ppr, fppg_ppr) AS name_label,
    IIF(
        (ROW_NUMBER() OVER(PARTITION BY c_year, c_pos ORDER BY pick_accuracy DESC) <= 3
         OR ROW_NUMBER() OVER(PARTITION BY c_year, c_pos ORDER BY pick_accuracy ASC) <= 3),
        name || '<br>' || c_pos || adp_pos_rank ||' to ' ||
        actual_pos_fin_fppg_ppr || ' (' || pick_accuracy || ') ppg',
        '') AS label
FROM nfl_adp_hype
WHERE 1=1
    AND c_pos IN ("QB", "WR", "RB", "TE")
    AND fppg_ppr IS NOT NULL
    AND (
        (draft_rank IS NOT NULL AND expected_ppg IS NOT NULL)
        OR actual_pos_fin_fppg_ppr < 60 --This leaves the opportunity for undrafted breakouts
        )
ORDER BY CAST(c_year AS INT) ASC, c_pos ASC, draft_rank ASC