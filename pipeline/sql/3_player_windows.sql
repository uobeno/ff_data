SELECT
    *,
    -- Career related stats
    MIN(year) OVER(PARTITION BY player_id) AS fyd,
    MAX(year) OVER(PARTITION BY player_id) AS lyd,
    year - MIN(year) OVER(PARTITION BY player_id) AS yid,
    LEAD(ROUND(fantasy_points / (g*1.0),2)) OVER (PARTITION BY player_id ORDER BY year ASC) AS next_fppg,
    ROUND(
        (LEAD(ROUND(fantasy_points / (g*1.0),2)) OVER (PARTITION BY player_id ORDER BY year ASC)
        / ROUND(fantasy_points / (g*1.0),2)) - 1
        ,4) AS next_fppg_growth,
    LEAD(ROUND(fantasy_points_ppr / g)) OVER (PARTITION BY player_id ORDER BY year ASC) AS next_fppg_ppr
FROM nfl_adp_names