/*
We're going to calculate the historical performance for a given ADP
based on the ACTUAL rb1 finish. 
The assumption there is that when you are drafting the RB1, you want the RB1
performance, not the average expectaction for the drafted RB1.
If you calculate it based on draft position, it includes players that
we got wrtong, which you shouldn't expect.

TODO: 
We could likely do this before this point, but we have to wait to do the window functions.
*/
DROP TABLE IF EXISTS hist_adp_perf;
CREATE TABLE hist_adp_perf AS 
SELECT
    actual_pos_fin_fppg_ppr,
    fantasy_pos,
    fantasy_pos || actual_pos_fin_fppg_ppr AS pos_w_fppg_ppr_finish,
    ROUND(AVG(fppg_ppr),2) AS exp_fppg_ppr,
    COUNT(1) AS n_in_exp_fppg_ppr
FROM nfl_window_stats
WHERE 1=1
    AND fantasy_pos IS NOT NULL
    AND fantasy_pos != 'FB'
GROUP BY 1, 2, 3
;

DROP TABLE IF EXISTS nfl_adp_hype;
CREATE TABLE nfl_adp_hype AS 
SELECT
    nfl.*,
    n_in_exp_fppg_ppr,
    exp_fppg_ppr,
    ROUND(exp_fppg_ppr - prior_fppg_ppr,2) AS pick_hype,
    IFNULL(ROUND(fppg_ppr - exp_fppg_ppr,2),0) AS pick_accuracy,
    CASE
        WHEN team != team_year_prior AND team LIKE '%TM' THEN 'In season trade'
        WHEN team != team_year_prior THEN 'New team - ffy'
        ELSE ''
        END AS team_change,
    -- Calculate the player rank among the position group on their own
    ROW_NUMBER() OVER(PARTITION BY c_year, c_pos, c_team
        ORDER BY fantasy_points_ppr DESC) AS depth_rank_tot,
    ROW_NUMBER() OVER(PARTITION BY c_year, c_pos, c_team
        ORDER BY fppg_ppr DESC) AS depth_rank_ppg_ppr,
    -- Ignore null draft position so they aren't ranked as the first drafted
    IIF(adp_ovr IS NULL, NULL,
        ROW_NUMBER() OVER(PARTITION BY c_year, c_pos, c_team
        ORDER BY IIF(adp_ovr IS NULL,500,adp_ovr) ASC)) AS depth_rank_adp
    -- TODO: look at when we expected one order and the order was different than expected
FROM nfl_window_stats nfl
LEFT OUTER JOIN hist_adp_perf hist
ON nfl.adp_pos = hist.pos_w_fppg_ppr_finish
;