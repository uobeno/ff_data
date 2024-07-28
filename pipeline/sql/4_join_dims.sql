nfl_adp_names
LEFT JOIN historical performance
LEFT JOIN team ranks
LEFT JOIN player share
LEFT JOIN other dimensions

-- Derived window stats, simplify this so that we
-- Can calculate change in one vs the other
ROUND(
        (LEAD(ROUND(fantasy_points / (g*1.0),2)) OVER (PARTITION BY player_id ORDER BY year ASC)
        / ROUND(fantasy_points / (g*1.0),2)) - 1
        ,4) AS next_fppg_growth,