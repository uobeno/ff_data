SELECT
    c_year AS year,
    c_pos AS position,
    name,
    dr10 AS round,
    exp_fppg_ppr AS fppg_ppr
FROM (
    SELECT
        *,
        -- It is never optimal to select anything but the best player for that position in that round
        -- This dramaticaly reduces the number of possibilities that we have to consider
        ROW_NUMBER() OVER(PARTITION BY c_year, c_pos, dr10 ORDER BY exp_fppg_ppr DESC) AS best_in_rnd
    FROM nfl_adp_hype
    )
WHERE 1=1
    AND c_pos IN ("QB", "WR", "RB", "TE")
    AND dr10 IS NOT NULL
    AND CAST(dr10 AS INT) <= 10
    AND c_year = '2024'
    AND best_in_rnd = 1
;