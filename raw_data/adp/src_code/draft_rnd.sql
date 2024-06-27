SELECT
    year,
    -- add the football position that they play
    IIF(LOWER(pos) LIKE 'k%', substring(pos,1,1),substring(pos,1,2)) AS fpos,
    -- add the pick that someone was in each round
        -- ((rank - 1) % 10) + 1 AS dr10_pick,
    -- add the round someone was picked in a 10 team league
    SUBSTRING(
        (rank + 9) / 10,
        1,
        instr((rank + 9) / 10,".") - 1
        ) AS dr10,
    -- we can add the pick and round for a 12 team leage here too if that's useful
    -- (rank + 11) / 12 AS dr12
    COUNT(1) AS player_cnt
FROM historical_adp
WHERE 1=1
    AND (
        pos LIKE 'WR%'
        OR pos LIKE 'RB%'
        OR pos LIKE 'QB%'
        OR pos LIKE 'TE%'
        )
    -- in the first 20 rounds
    AND (rank + 9) / 10 < 20
GROUP BY 1, 2, 3
ORDER BY 1, 2, 3
;