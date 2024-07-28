DROP TABLE IF EXISTS nfl_window_stats;
CREATE TABLE nfl_window_stats AS
SELECT
    *,
    -- Career related stats
    -- Add the first year we saw the player
    MIN(year) OVER(PARTITION BY name) AS fyd,
    -- The last year that we saw the player
    MAX(year) OVER(PARTITION BY name) AS lyd,
    -- The year in data that this season is
    -- First year is year 1
    -- Rookie year is year 1 for everyone except the first season in the datatset
    (c_year + 1) - MIN(c_year) OVER(PARTITION BY name) AS yid,

    -- Add in next year stats
    LEAD(fppg) OVER (PARTITION BY name ORDER BY c_year ASC) AS next_fppg,
    LEAD(fppg_ppr) OVER (PARTITION BY name ORDER BY c_year ASC) AS next_fppg_ppr,
    -- Add in prior year stats
    IFNULL(LAG(fppg) OVER (PARTITION BY name ORDER BY c_year ASC),0) AS prior_fppg,
    IFNULL(LAG(fppg_ppr) OVER (PARTITION BY name ORDER BY c_year ASC),0) AS prior_fppg_ppr,

    -- Add the team that the player was on the year before and year after this year
    -- Note that a trade tags a player with "2TM" or "3TM"
    -- TODO:
    -- figure out when teams change name (SDG -> LAC, OAK -> LVR)
    -- Also, david johnson didn't go from PIT -> ARI
    -- Also, in the adp data a lot of the team names are different, that's ok!
    LAG(c_team) OVER(PARTITION BY name ORDER BY c_year ASC) AS team_year_prior,
    LEAD(c_team) OVER(PARTITION BY name ORDER BY c_year ASC) AS team_next_year,
    -- Fill the players team in that year with their last team when they got traded
    -- This allows us to rollup stats on a team and allocate them to one of them
    IIF(c_team LIKE '%TM',LAG(c_team) OVER(PARTITION BY name ORDER BY c_year ASC),c_team) AS fill_team,

    -- TODO:
    -- Could add in thing like next year yards, targets, etc, but then the table gets massive
    -- We might want to predict taht stuff, but let's do it later on

    -- Calculate the fantasy finish based on different points
    ROW_NUMBER() OVER(PARTITION BY year, fantasy_pos ORDER BY fppg_ppr DESC) AS actual_pos_fin_fppg_ppr,
    ROW_NUMBER() OVER(PARTITION BY year, fantasy_pos ORDER BY fppg DESC) AS actual_pos_fin_fppg_std,
    ROW_NUMBER() OVER(PARTITION BY year, fantasy_pos ORDER BY fantasy_points_ppr DESC) AS actual_pos_fin_tot_ppr,
    ROW_NUMBER() OVER(PARTITION BY year, fantasy_pos ORDER BY fantasy_points DESC) AS actual_pos_fin_tot_std
FROM nfl_adp_names
;