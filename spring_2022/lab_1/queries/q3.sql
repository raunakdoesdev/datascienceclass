-- Write your query here.
SELECT titles.title_id, titles.primary_title, COUNT(DISTINCT crew.person_id) AS num_actors
FROM titles, crew
WHERE
    titles.title_id = crew.title_id
    AND titles.type = 'movie'
    AND (crew.category = 'actor' OR crew.category = 'actress')
GROUP BY titles.title_id
ORDER BY num_actors DESC, titles.primary_title ASC
LIMIT 1;