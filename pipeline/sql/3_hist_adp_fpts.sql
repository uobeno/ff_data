%%sql
DROP TABLE IF EXISTS nfl_adp_hype;
CREATE TABLE nfl_adp_hype AS 
WITH nfl AS (
SELECT
    name AS cleaned_player,
    c_year AS year,
    COALESCE(fantasy_pos,SUBSTRING(ADP_POS,1,2)) AS fantasy_pos,
    adp_pos,
    fppg_ppr,
    yid,
    ROW_NUMBER() OVER(PARTITION BY year, fantasy_pos ORDER BY fppg_ppr DESC) AS actual_pos_finish,
    ifnull(LAG(fppg_ppr) OVER(PARTITION BY name ORDER BY c_year ASC),0) AS prior_year_fppg
FROM nfl_adp_names nlf
WHERE 1=1
    AND (fantasy_pos != 'FB' OR fantasy_pos IS NULL)
)
SELECT
    cleaned_player,
    year,
    yid,
    fantasy_pos,
    adp_pos,
    fppg_ppr_rank AS adp_pos_n,
    actual_pos_finish,
    avg_fppg_ppr AS expect_adp_ppg,
    prior_year_fppg,
    ROUND(avg_fppg_ppr - prior_year_fppg,2) AS hype,
    fppg_ppr AS actual_fppg_ppr,
    IFNULL(ROUND(fppg_ppr - avg_fppg_ppr,2),0) AS performance
FROM nfl
LEFT OUTER JOIN (
    SELECT
        fppg_ppr_rank,
        fantasy_pos || fppg_ppr_rank AS exp_pos,
        ROUND(AVG(fppg_ppr),2) AS avg_fppg_ppr
    FROM (
        SELECT
            fantasy_pos,
            ROW_NUMBER() OVER(PARTITION BY year, fantasy_pos ORDER BY fppg_ppr DESC) AS fppg_ppr_rank,
            fppg_ppr
        FROM nfl_enhanced
        WHERE 1=1
            AND fantasy_pos != 'FB'
        )
    GROUP BY 1, 2
    ) hist
ON nfl.adp_pos = hist.exp_pos