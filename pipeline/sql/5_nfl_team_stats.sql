DROP TABLE IF EXISTS nfl_position_groups;
CREATE TABLE nfl_position_groups AS
SELECT
    fill_team AS team,
    c_year,
    c_pos,
    -- OVERALL ADP FOR THE PLAYER IN DEPTH 1, 2, 3 OF EACH POSITION GROUP FOR THAT TEAM
    MIN((IIF(depth_rank_adp=1,adp_ovr,NULL))) AS adp_ovr_depth1,
    MIN((IIF(depth_rank_adp=2,adp_ovr,NULL))) AS adp_ovr_depth2,
    MIN((IIF(depth_rank_adp=3,adp_ovr,NULL))) AS adp_ovr_depth3,
    -- AGE OF THE PLAYER FOR THE ADP OF 1, 2, 3 ON EACH POSITION GROUP
    MIN((IIF(depth_rank_adp=1,age,NULL))) AS age_depth1,
    MIN((IIF(depth_rank_adp=2,age,NULL))) AS age_depth2,
    MIN((IIF(depth_rank_adp=3,age,NULL))) AS age_depth3,
    -- GAMES PLAYED FOR THE ADP OF 1, 2, 3 ON EACH TEAMS POSITION GROUP
    MIN((IIF(depth_rank_adp=1,g,NULL))) AS g_depth1,
    MIN((IIF(depth_rank_adp=2,g,NULL))) AS g_depth2,
    MIN((IIF(depth_rank_adp=3,g,NULL))) AS g_depth3,
    -- ADP OF THE PLAYERS POSITION GROUP FOR THE 1, 2, 3RD RANKED DEPTH ON EACH TEAM
    MIN((IIF(depth_rank_adp=1,adp_pos_rank,NULL))) AS adp_pos_rank_d1,
    MIN((IIF(depth_rank_adp=2,adp_pos_rank,NULL))) AS adp_pos_rank_d2,
    MIN((IIF(depth_rank_adp=3,adp_pos_rank,NULL))) AS adp_pos_rank_d3,
    -- THE SEASON OF THE PLAYER IN ADP RANK 1, 2, 3
    MIN((IIF(depth_rank_adp=1,yid,NULL))) AS yid_d1,
    MIN((IIF(depth_rank_adp=2,yid,NULL))) AS yid_d2,
    MIN((IIF(depth_rank_adp=3,yid,NULL))) AS yid_d3,
    -- QB STATS
    SUM(pass_cmp) AS tot_pass_cmp,
    SUM(pass_att) AS tot_pass_att,
    SUM(pass_yds) AS tot_pass_yds,
    SUM(pass_td) AS tot_pass_td,
    SUM(pass_int) AS tot_pass_int,
    -- RB STATS
    SUM(rush_att) AS tot_rush_att,
    SUM(rush_yds) AS tot_rush_yds,
    SUM(rush_td) AS tot_rush_td,
    -- WR STATS
    SUM(targets) AS tot_targets,
    SUM(rec) AS tot_rec,
    SUM(rec_yds) AS tot_rec_yds,
    SUM(rec_td) AS tot_rec_td,
    -- OTHER 
    SUM(fumbles) AS tot_fumbles,
    SUM(fumbles_lost) AS tot_fumbles_lost,
    SUM(all_td) AS tot_all_td,
    -- POINTS
    SUM(fantasy_points_ppr) AS tot_fantasy_points_ppr,
    SUM(fppg_ppr) AS tot_fppg_ppr,
    SUM(exp_fppg_ppr) AS tot_exp_fppg_ppr,
    SUM(pick_hype) AS tot_pick_hype,
    SUM(pick_accuracy) AS tot_pick_accuracy,
    -- OTHER
    -- NUMBER OF PLAYERS TRADED
    SUM(IIF(team_change IS NOT NULL,1,0)) AS cnt_team_change
FROM nfl_adp_hype
GROUP BY 1, 2, 3
;

-- we will be able to get player share of position group stats when we join
-- this back to the main table, so that isn't a massive focus right now
-- however, we can look at position group total so we can get share of team total 
-- we can also use this opportunity to pivot data that might be useful for depth chart movement
-- things like, when the actual outcome is differnt than adp, was the player older or younger than 
-- the person they surpassed?
-- or, does a higher drafted qb mean good production for the entire offense?
