/*
THIS FILE GRADES THE RESULTS OF COMBOS TABLE
THAT HAS A COMBO OF EVERY POSSIBLE TEAM
*/
SELECT
    c_year AS year,
    c_pos AS position,
    name,
    g AS games,
    dr10 AS round,
    fppg_ppr
FROM nfl_adp_hype
WHERE 1=1
    AND c_pos IN ("QB", "WR", "RB", "TE")
    AND fppg_ppr IS NOT NULL
    AND dr10 IS NOT NULL
    AND CAST(dr10 AS INT) <= 5
    AND c_year = '2023'
;