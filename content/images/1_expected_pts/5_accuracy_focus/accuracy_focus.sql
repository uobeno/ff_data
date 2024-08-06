SELECT
    year,
    position,
    name,
    name_label,
    label
FROM image_ep_1_accuracy_graph
WHERE 1=1
    AND label != ''
ORDER BY CAST(year AS INT) ASC, position ASC, draft_rank ASC