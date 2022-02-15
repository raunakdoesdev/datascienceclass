-- Write your query here.
/*
 (Simple subquery/CTE, 10 pts) Find the movie with the most actors and actresses (cumulatively). Unlike in question (3),
 you should return all such movies. Again, return the title_id, primary title and number of actors. Order by primary
 title (ascending).
 */
WITH movies as (
  SELECT titles.title_id,
    titles.primary_title,
    COUNT(crew.person_id) AS num_actors
  FROM titles,
    crew
  WHERE titles.title_id = crew.title_id
    AND titles.type = 'movie'
    AND (
      crew.category = 'actor'
      OR crew.category = 'actress'
    )
  GROUP BY titles.title_id
)
SELECT title_id,
  primary_title,
  num_actors
FROM movies
WHERE num_actors = (
    SELECT MAX(num_actors)
    FROM movies
  )
ORDER BY primary_title ASC;