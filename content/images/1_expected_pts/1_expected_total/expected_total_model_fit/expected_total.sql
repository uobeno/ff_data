SELECT
    fantasy_pos AS position,
    CAST(actual_pos_fin_fppg_ppr AS INT) AS rank,
    exp_fppg_ppr AS avg_ppr_ppg
FROM hist_adp_perf
WHERE 1=1
    AND CAST(actual_pos_fin_fppg_ppr AS INT) < 100
    AND NOT (
        fantasy_pos = 'QB'
        AND CAST(actual_pos_fin_fppg_ppr AS INT) > 60
    )
ORDER BY 1, 2