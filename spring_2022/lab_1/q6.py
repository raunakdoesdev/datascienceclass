import pandas as pd

"""
WITH movies as (
  SELECT titles.title_id,
    titles.primary_title,
    COUNT(DISTINCT crew.person_id) AS num_actors
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
"""

nrows = None
titles = pd.read_pickle("data/titles.pkl")
crew = pd.read_pickle("data/crew.pkl")

# Filter
titles = titles[titles["type"] == "movie"]
crew = crew[crew["category"].isin(["actor", "actress"])]

# Join
movies = titles.merge(crew, on="title_id").groupby("title_id").agg({"person_id": "count", "primary_title": "first"})
movies = movies[movies["person_id"] == movies["person_id"].max()]
return movies.sort_values(by="primary_title", ascending=True).reset_index(drop=True)
