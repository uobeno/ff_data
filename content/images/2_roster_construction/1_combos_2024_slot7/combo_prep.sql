SELECT
    c_year AS year,
    c_pos AS position,
    name,
    dr10_adj AS round,
    exp_fppg_ppr AS fppg_ppr
FROM (
    SELECT
        *,
        -- It is never optimal to select anything but the best player for that position in that round
        -- This dramaticaly reduces the number of possibilities that we have to consider
        ROW_NUMBER() OVER(PARTITION BY c_year, c_pos, dr10_adj ORDER BY exp_fppg_ppr DESC) AS best_in_rnd
    FROM (
        SELECT
            *,
            CASE
                -- Adjust the round for draft slot 7
                WHEN adp_ovr < 4 THEN 0
                -- Even round adjustment
                WHEN (CAST(dr10 AS INT) % 2 != 1) AND dr10_pick <= 2 THEN dr10 - 1
                -- Odd round adjustment
                WHEN (CAST(dr10 AS INT) % 2 = 1) AND dr10_pick <= 5 AND dr10 != '1' THEN dr10 - 1
                ELSE CAST(dr10 AS INT)
                END AS dr10_adj
        FROM nfl_adp_hype
        )
    WHERE 1=1
        AND dr10_adj != 0
    )
WHERE 1=1
    AND c_pos IN ("QB", "WR", "RB", "TE")
    AND dr10 IS NOT NULL
    AND CAST(dr10 AS INT) <= 10
    AND c_year = '2024'
    AND best_in_rnd = 1
;