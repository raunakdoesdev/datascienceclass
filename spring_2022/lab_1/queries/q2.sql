-- Write your query here.
SELECT titles.title_id,
    titles.primary_title AS name,
    ratings.rating
FROM titles,
    ratings
WHERE titles.title_id = ratings.title_id
    AND titles.type = 'tvSeries'
    AND titles.genres LIKE "%Action%"
    AND titles.premiered == 2021
    AND ratings.rating >= 8
    AND ratings.votes >= 100
ORDER BY ratings.rating DESC,
    titles.primary_title ASC;