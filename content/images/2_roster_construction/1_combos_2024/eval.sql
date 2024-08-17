SELECT
    *,
    CASE
        WHEN position IN ('QB', 'TE') AND pos_rank = 1 THEN fppg_ppr
        WHEN position IN ('RB', 'WR') AND pos_rank <= 2 THEN fppg_ppr
        -- The 5th ranked non qb is your flex. A QB will never be ranked 5th unless 5 on is all QBs
        WHEN position IN ('RB', 'WR', 'TE') AND rank_on_team = 5 THEN fppg_ppr
        ELSE 0
        END AS team_score
FROM (
    SELECT
        *,
        ROW_NUMBER() OVER(PARTITION BY year, team_id, position ORDER BY fppg_ppr DESC) AS pos_rank,
        ROW_NUMBER() OVER(
            PARTITION BY year, team_id 
            ORDER BY IIF(position = 'QB', 0, fppg_ppr) DESC) AS rank_on_team,
        -- Add in position count totals so we can only grade valid teams
        SUM(IIF(position = 'QB', 1, 0)) OVER(PARTITION BY team_id) AS qb_cnt,
        SUM(IIF(position = 'RB', 1, 0)) OVER(PARTITION BY team_id) AS rb_cnt,
        SUM(IIF(position = 'WR', 1, 0)) OVER(PARTITION BY team_id) AS wr_cnt,
        SUM(IIF(position = 'TE', 1, 0)) OVER(PARTITION BY team_id) AS te_cnt
    FROM draft_combos_dr10_2024
)
WHERE 1=1
    -- enforce position total required to be a valid team
    AND qb_cnt >= 1
    AND rb_cnt >= 2
    AND wr_cnt >= 2
    AND te_cnt >= 1
;