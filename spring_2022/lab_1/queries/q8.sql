/*
 (SQL Only: Window Functions, 10 pts) For each year, find the top 3 actors that appear in the most number of above
 average movies (with a rating >= 5). If multiple actors are tied in the top, return all of them. Return the year,
 the name, number of above average movies, and the ranking. Sort by year (ascending), ranking (ascending) and name
 (ascending) to break ties.
 */
WITH base_table AS (
    SELECT premiered as year,
        "name",
        COUNT(titles.title_id) as num_movies
    FROM titles,
        people,
        crew,
        ratings
    WHERE titles.title_id = crew.title_id
        AND people.person_id = crew.person_id
        AND (
            crew.category = 'actor'
            OR crew.category = 'actress'
        )
        AND titles.type = 'movie'
        AND ratings.title_id = titles.title_id
        AND ratings.rating >= 5
    GROUP BY year,
        crew.person_id
)
SELECT *
FROM (
        SELECT year,
            name,
            num_movies,
            RANK() OVER (
                PARTITION BY year
                ORDER BY num_movies DESC
            ) AS rank
        FROM base_table
    )
WHERE rank <= 3
ORDER BY year ASC,
    rank ASC,
    name ASC;