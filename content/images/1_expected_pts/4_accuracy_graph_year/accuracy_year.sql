SELECT
    c_year AS year,
    c_pos AS position,
    adp_pos_rank AS draft_rank,
    fppg_ppr AS points_scored
FROM nfl_adp_hype
WHERE 1=1
    AND c_pos IN ("QB", "WR", "RB", "TE")
    AND fppg_ppr IS NOT NULL
    AND (
        (draft_rank IS NOT NULL AND fppg_ppr IS NOT NULL)
        )
    AND (
        (c_pos IN ("QB", "TE") AND CAST(adp_pos_rank AS INT) <= 20)
        OR (c_pos IN ("WR", "RB") AND CAST(adp_pos_rank AS INT) <= 50)
    )
UNION ALL
SELECT
    'draft avg' AS year,
    c_pos AS position,
    adp_pos_rank AS draft_rank,
    AVG(fppg_ppr) AS points_scored
FROM nfl_adp_hype
WHERE 1=1
    AND c_pos IN ("QB", "WR", "RB", "TE")
    AND fppg_ppr IS NOT NULL
    AND (
        (draft_rank IS NOT NULL AND fppg_ppr IS NOT NULL)
        )
    AND (
        (c_pos IN ("QB", "TE") AND CAST(adp_pos_rank AS INT) <= 20)
        OR (c_pos IN ("WR", "RB") AND CAST(adp_pos_rank AS INT) <= 50)
    )
GROUP BY 1, 2, 3
UNION ALL
SELECT
    'draft avg' AS year,
    c_pos AS position,
    adp_pos_rank AS draft_rank,
    AVG(fppg_ppr) AS points_scored
FROM nfl_adp_hype
WHERE 1=1
    AND c_pos IN ("QB", "WR", "RB", "TE")
    AND fppg_ppr IS NOT NULL
    AND (
        (draft_rank IS NOT NULL AND fppg_ppr IS NOT NULL)
        )
    AND (
        (c_pos IN ("QB", "TE") AND CAST(adp_pos_rank AS INT) <= 20)
        OR (c_pos IN ("WR", "RB") AND CAST(adp_pos_rank AS INT) <= 50)
    )
GROUP BY 1, 2, 3
UNION ALL 
SELECT
    'finish avg' AS year,
    fantasy_pos AS position,
    actual_pos_fin_fppg_ppr AS draft_rank,
    exp_fppg_ppr AS points_scored
FROM hist_adp_perf
WHERE 1=1
    AND (
        (fantasy_pos IN ("QB", "TE") AND CAST(actual_pos_fin_fppg_ppr AS INT) <= 20)
        OR (fantasy_pos IN ("WR", "RB") AND CAST(actual_pos_fin_fppg_ppr AS INT) <= 50)
    )