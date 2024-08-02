SELECT
    fantasy_pos AS position,
    MAX(IIF(actual_pos_fin_fppg_ppr = 1, exp_fppg_ppr,0)) AS expected_1,
    MAX(IIF(actual_pos_fin_fppg_ppr = 20, exp_fppg_ppr,0)) AS expected_20,
    ROUND((MAX(IIF(actual_pos_fin_fppg_ppr = 1, exp_fppg_ppr,0)) - 
    MAX(IIF(actual_pos_fin_fppg_ppr = 20, exp_fppg_ppr,0))),2) AS drop_off
FROM hist_adp_perf
WHERE 1=1
    AND (actual_pos_fin_fppg_ppr = 1 OR actual_pos_fin_fppg_ppr = 20)
GROUP BY 1
ORDER BY 1