DROP TABLE IF EXISTS enhanced_adp;
CREATE TABLE enhanced_adp AS
SELECT
    *,
    IIF( -- Parse the football position out of the position like WR1 or RB10
        LOWER(pos) LIKE 'k%',
        substring(pos,1,1), --Only grab the first character for kicker
        substring(pos,1,2) --Grab the first two characters for all other
        ) AS fpos,
    -- The pick number that someone was in a round based on 10 team league
    ((rank - 1) % 10) + 1 AS dr10_pick,
    SUBSTRING( -- add the round someone was picked in a 10 team league
        (rank + 9) / 10,
        1,
        instr((rank + 9) / 10,".") - 1 -- only grab the FIRST digit to get the round
        ) AS dr10
FROM historical_adp
WHERE 1=1
    AND year > 2015
;
