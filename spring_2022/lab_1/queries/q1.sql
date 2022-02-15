-- Write your query here.
-- Compute the number of distinct actors and actresses

SELECT
    category,
    COUNT(DISTINCT person_id) AS num_actors
FROM crew
WHERE
    category = 'actor' OR category = 'actress'
GROUP BY
    category;
-- WHERE category = 'actor' OR category = 'actress';