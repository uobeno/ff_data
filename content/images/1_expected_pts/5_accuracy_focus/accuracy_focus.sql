SELECT
    *
FROM image_ep_1_accuracy_graph
WHERE 1=1
    AND label != ''
    AND NOT (year='2016' AND name = 'david johnson')
    AND pick_accuracy < 0
    AND (
        position='QB' AND draft_rank < 20
        OR position!='QB')
ORDER BY pick_accuracy ASC
LIMIT 20