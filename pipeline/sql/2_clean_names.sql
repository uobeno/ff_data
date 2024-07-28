-- Separate the ADP players that we want to join to NFL data
DROP TABLE IF EXISTS adp_join_prep;
CREATE TABLE adp_join_prep AS
WITH join_prep AS (
SELECT
    player AS adp_player,
    rank AS adp_ovr,
    team AS adp_team,
    POS AS adp_pos,
    year AS adp_year,
    AVG AS adp_avg
FROM enhanced_adp 
WHERE 1=1
    AND player IS NOT NULL
    AND NOT pos LIKE 'DST%'
    AND NOT pos LIKE 'K%'
    AND CAST(year AS INT) > 2015
)
SELECT * FROM join_prep
;

-- Clean the nfl names
-- Clean the adp names
-- Join the cleaned values together
-- Retain the nfl and adp keys we want to link to the join key
-- Treat special cases by 
DROP TABLE IF EXISTS name_map;
CREATE TABLE name_map AS 
WITH nfl AS (
    SELECT DISTINCT
        TRIM(cleaned_player) AS trim_nfl_og,
        TRIM(
            REPLACE(
                REPLACE(
                    LOWER(
                        REPLACE(
                            REPLACE(
                                REPLACE(
                                    REPLACE(
                                        cleaned_player
                                        , ".",'')
                                     ,"III",'')
                            ,"II",'')
                        , "'",'')
                    )
                , 'jr', '')
            , 'sr', '')
        ) AS nfl_clean
    FROM nfl_enhanced nfl
),
adp AS (
    SELECT DISTINCT
        TRIM(adp_player) AS trim_adp_og,
        TRIM(
            REPLACE(
                REPLACE(
                    LOWER(
                        REPLACE(
                            REPLACE(
                                REPLACE(
                                    REPLACE(adp_player, "'",'')
                                    ,"III",'')
                                , " II",'')
                            , ".",'')
                    )
                , ' jr', '')
            , ' sr', '')
        ) AS adp_clean
    FROM adp_join_prep nfl
)
SELECT DISTINCT
    trim_adp_og,
    trim_nfl_og,
    adp_clean,
    nfl_clean,
    CASE
        WHEN trim_nfl_og = 'Marquise Brown' THEN 'hollywood brown'
        WHEN trim_adp_og = 'Gabe Davis' THEN 'gabriel davis'
        WHEN trim_adp_og = 'William Fuller V' THEN 'will fuller'
        WHEN trim_adp_og = 'William Fuller' THEN 'will fuller'
        WHEN trim_adp_og = 'Robby Anderson' THEN 'robbie chosen'
        ELSE COALESCE(adp_clean,nfl_clean)
        END AS name
FROM adp adp
FULL OUTER JOIN nfl nfl
ON adp_clean = nfl_clean
;

-- Add the cleaned name that we want to join on to the adp table
DROP TABLE IF EXISTS nfl_adp_name_adp;
CREATE TABLE nfl_adp_name_adp AS
SELECT
    adp.*,
    name.name AS adp_join_name
FROM adp_join_prep adp
LEFT OUTER JOIN (
    SELECT DISTINCT
        trim_adp_og,
        name
    FROM name_map
    ) name
ON TRIM(adp.adp_player) = name.trim_adp_og
;

-- Add the cleaned name that we want to join on to the nfl table
DROP TABLE IF EXISTS nfl_adp_name_nfl;
CREATE TABLE nfl_adp_name_nfl AS
SELECT
    nfl.*,
    name.name AS nfl_join_name
FROM nfl_enhanced nfl
LEFT OUTER JOIN (
    SELECT DISTINCT
        trim_nfl_og,
        name
    FROM name_map
    ) name
ON TRIM(nfl.cleaned_player) = name.trim_nfl_og
;

DROP TABLE IF EXISTS nfl_adp_names;
CREATE TABLE nfl_adp_names AS
SELECT
    adp.*,
    nfl.*,
    COALESCE(adp_join_name,nfl_join_name) AS name,
    COALESCE(cleaned_player,adp_player) AS c_player,
    COALESCE(year,adp_year) AS c_year
FROM nfl_adp_name_adp adp
FULL OUTER JOIN nfl_adp_name_nfl nfl
    ON nfl.year = adp.adp_year
    AND TRIM(nfl.nfl_join_name) = adp.adp_join_name
;