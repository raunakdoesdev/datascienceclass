WITH split(title_id, genre, str) AS (
    SELECT title_id,
        '',
        genres || ','
    FROM (
            SELECT *
            FROM titles
            WHERE "type" = 'movie'
        )
    UNION ALL
    SELECT title_id,
        substr(str, 0, instr(str, ',')),
        substr(str, instr(str, ',') + 1)
    FROM split
    WHERE str != ''
),
movies AS (
    SELECT AVG(ratings.rating) AS average_rating,
        genre
    FROM split,
        ratings
    WHERE genre != ""
        AND genre != '\N'
        AND split.title_id = ratings.title_id
    GROUP BY genre
)
SELECT genre,
    average_rating
FROM movies
ORDER BY average_rating DESC,
    genre ASC;