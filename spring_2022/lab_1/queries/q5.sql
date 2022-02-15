-- Write your query here.
WITH actors as (
    SELECT crew.category,
        crew.person_id,
        COUNT(crew.person_id) AS num_appearances
    FROM crew,
        titles
    WHERE crew.title_id = titles.title_id
        AND titles.type = "movie"
        AND (
            crew.category = "actor"
            OR crew.category = "actress"
        )
    GROUP BY crew.person_id
)
SELECT actors.category,
    people.name,
    actors.num_appearances
FROM actors,
    people
WHERE actors.person_id = people.person_id
    AND actors.num_appearances = (
        SELECT MAX(num_appearances)
        FROM actors
    )
ORDER BY people.name ASC;