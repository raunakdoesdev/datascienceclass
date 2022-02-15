WITH good_stuff AS (
    SELECT titles.type,
        titles.primary_title AS "name",
        ratings.rating
    FROM titles,
        ratings
    WHERE ratings.title_id = titles.title_id
        AND (
            titles.type = 'movie'
            OR titles.type = 'tvSeries'
        )
        AND ratings.rating >= 8
        AND ratings.votes >= 100
        AND titles.premiered = 2021
)
SELECT "type",
    "name",
    rating,
    RANK() OVER (
        PARTITION BY good_stuff.type
        ORDER BY rating DESC,
            "name" ASC
    ) AS rank
FROM good_stuff
ORDER BY "type" ASC,
    rating DESC,
    "name" ASC;