-- Write your query here.
WITH actors as (
    SELECT people.name,
        COUNT(crew.person_id) AS num_appearances,
        AVG(ratings.rating) AS average_rating
    FROM crew,
        titles,
        ratings,
        people
    WHERE crew.title_id = titles.title_id
        AND ratings.title_id = titles.title_id
        AND people.person_id = crew.person_id
        AND titles.type = "movie"
        AND (
            crew.category = "actor"
            OR crew.category = "actress"
        )
    GROUP BY crew.person_id
)
SELECT *
FROM actors
WHERE num_appearances = 5
    AND average_rating = (
        SELECT MAX(average_rating)
        FROM actors
        WHERE num_appearances = 5
    );