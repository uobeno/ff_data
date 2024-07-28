%%sql
DROP TABLE IF EXISTS nfl_enhanced;
CREATE TABLE nfl_enhanced AS 
SELECT
    *,
    -- Clean up the player name
    REPLACE(REPLACE(player,'*',''),'+','') AS cleaned_player,
    IIF(INSTR(player, '*') > 0, 'true', 'false') AS pro_bowl,
    IIF(INSTR(player, '+') > 0, 'true', 'false') AS all_pro,
    
    -- Per game fantasy points & half PPR
    ROUND(fantasy_points / (g*1.0),2) AS fppg,
    ROUND(fantasy_points / (gs*1.0),2) AS fppgs,
    ROUND(fantasy_points_ppr / (g*1.0),2) AS fppg_ppr,
    fantasy_points + (rec * 0.5) AS fantasy_points_hppr,
    ROUND(g / (IIF(year >= 2021, 17, 16)*1.00),2) AS pgp,

    -- Per game attempts and volume
    ROUND(pass_att / (g*1.0),2) AS pass_att_pg,
    ROUND(rush_att / (g*1.0),2) AS rush_att_pg,
    ROUND(targets / (g*1.0),2) AS targets_pg,

    -- Per game output and rates
        -- QB
        ROUND(pass_cmp / (g*1.0),2) AS pass_cmp_pg,
        ROUND(pass_yds / (g*1.0),2) AS pass_yds_pg,
        ROUND(pass_td / (g*1.0),3) AS pass_td_pg,
        ROUND(pass_td / (pass_att*1.0),4) AS pass_td_rate,
        ROUND(pass_att / (pass_td*1.0),2) AS pass_att_ptd,
    
        -- RB    
        ROUND(rush_td / (g*1.0),3) AS rush_td_pg,
        ROUND(rush_yds / (g*1.0),2) AS rush_yds_pg,
        ROUND(rush_yds / (rush_td*1.0),2) AS rush_yds_per_td,
        ROUND(rush_att / (rush_td*1.0),2) AS rush_att_per_td,
    
        -- WR
        ROUND(rec / (g*1.0),3) AS rec_pg,
        ROUND(rec / (targets*1.0),3) AS catch_rate,
        ROUND(rec_td / (g*1.0),4) AS rec_td_pg,
        ROUND(rec_yds / (g*1.0),2) AS rec_yds_pg,
        ROUND(targets / (rec_td*1.0),2) AS tar_per_td,
        ROUND(rec / (rec_td*1.0),2) AS rec_per_td,
        ROUND(rec_yds / (rec_td*1.0),2) AS rec_yds_per_td
FROM nfl_results