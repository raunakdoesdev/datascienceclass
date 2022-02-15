import argparse
import sqlite3 as sql

import pandas as pd

# nrows = 200
nrows = None


def runSQL(query_num, store):
    with sql.connect("data/imdb.db") as conn, open("queries/q{}.sql".format(query_num)) as in_query:
        cur = conn.cursor()
        df = pd.read_sql_query(in_query.read(), conn)
        pd.set_option("display.max_rows", 100)
        if store:
            df.to_csv(f"submission/sql_sol{query_num}.csv", index=False)
        return df


def Q1Pandas():
    crew = pd.read_csv("data/crew.csv", nrows=nrows)
    crew = crew[crew["category"].isin(["actor", "actress"])]
    crew = crew.groupby("category").nunique()["person_id"].to_frame()
    crew = crew.rename(columns={"person_id": "count"})
    crew["category"] = crew.index
    crew = crew.reset_index(drop=True)
    crew = crew.sort_values("category", ascending=True)[["category", "count"]]
    return crew.reset_index(drop=True)


def Q2Pandas():
    """
    (Simple filtering and join, 5 pts) Find the action TV shows (titles.type=tvSeries and titles.genres contains Action)
    released in 2021, with a rating >= 8 and at least 100 votes. Return title_id, name, and rating. Order by rating
    (descending) and then name (ascending) to break ties.
    """

    nrows = None
    titles = pd.read_csv("data/titles.csv", nrows=nrows)
    ratings = pd.read_csv("data/ratings.csv", nrows=nrows)
    titles = titles.merge(ratings, on="title_id")
    titles = titles[
        (titles["type"] == "tvSeries") & (titles["genres"].str.contains("Action")) & (titles["premiered"] == 2021)
    ]
    titles = titles[(titles["rating"] >= 8) & (titles["votes"] >= 100)]
    titles.rename({"primary_title": "name"}, axis=1, inplace=True)
    titles = titles[["title_id", "name", "rating"]].sort_values(["rating", "name"], ascending=[False, True])
    return titles.reset_index(drop=True)


def Q3Pandas():
    """
    (Simple aggregation and join, 10 pts) Find the movie (titles.type=movie) with the most actors and actresses
    (cumulatively). If multiple movies are tied, return the one with the alphabetically smallest primary title.
    Return the title_id, primary title, and number of actors.
    """
    titles = pd.read_csv("data/titles.csv", nrows=nrows)
    crew = pd.read_csv("data/crew.csv", nrows=nrows)

    # Filter
    titles = titles[titles["type"] == "movie"]
    crew = crew[crew["category"].isin(["actor", "actress"])]

    # Join
    movies = (
        titles.merge(crew, on="title_id")
        .groupby("title_id")
        .agg(num_actors=("person_id", "count"), primary_title=("primary_title", "first"))
        .sort_values(by=["num_actors", "primary_title"], ascending=[False, True])
    )
    movies["title_id"] = movies.index
    return movies.iloc[[0]][["title_id", "primary_title", "num_actors"]].reset_index(drop=True)


def Q4Pandas():
    """
    Find the movie with the most actors and actresses (cumulatively). Unlike in question (3),
    you should return all such movies. Again, return the title_id, primary title and number of actors.
    Order by primary title (ascending).
    """
    titles = pd.read_csv("data/titles.csv", nrows=nrows)
    crew = pd.read_csv("data/crew.csv", nrows=nrows)
    titles = titles[titles["type"] == "movie"]
    crew = crew[crew["category"].isin(["actor", "actress"])]
    movies = titles.merge(crew, on="title_id").groupby("title_id").agg({"person_id": "count", "primary_title": "first"})
    movies = movies[movies["person_id"] == movies["person_id"].max()]
    return movies.sort_values(by="primary_title", ascending=True).reset_index(drop=True)


def Q5Pandas():
    titles = pd.read_csv("data/titles.csv", nrows=nrows)
    crew = pd.read_csv("data/crew.csv", nrows=nrows)
    people = pd.read_csv("data/people.csv", nrows=nrows)
    actors = titles[titles["type"] == "movie"].merge(crew[crew["category"].isin(["actor", "actress"])], on="title_id")
    actors = actors.groupby("person_id").nunique()["title_id"].to_frame("num_appearances")
    actors = actors[actors["num_appearances"] == actors["num_appearances"].max()]
    actors = (
        actors.merge(people, on="person_id")
        .merge(crew, on="person_id")
        .sort_values(by="num_appearances", ascending=False)[["category", "name", "num_appearances"]]
    )
    return actors.drop_duplicates(subset=["name"]).reset_index(drop=True)


def Q6Pandas():
    titles = pd.read_csv("data/titles.csv", nrows=nrows)
    crew = pd.read_csv("data/crew.csv", nrows=nrows)
    people = pd.read_csv("data/people.csv", nrows=nrows)
    ratings = pd.read_csv("data/ratings.csv", nrows=nrows)

    # Filter
    titles = titles[titles["type"] == "movie"]
    crew = crew[crew["category"].isin(["actor", "actress"])]

    # Join
    actors = (
        titles.merge(ratings, on="title_id")
        .merge(crew, on="title_id")
        .merge(people, on="person_id")
        .groupby("person_id")
    ).agg({"title_id": "count", "rating": "mean", "name": "first"})
    actors = actors[actors["title_id"] == 5]
    actors = actors[actors["rating"] == actors["rating"].max()]
    return actors[["name", "title_id", "rating"]].reset_index(drop=True)


pandas_queries = [Q1Pandas, Q2Pandas, Q3Pandas, Q4Pandas, Q5Pandas, Q6Pandas]
df = None
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", "-q", help="Run a specific query", type=int)
    parser.add_argument("--store", "-s", help="Store", default=False, action="store_true")
    args = parser.parse_args()

    store = args.store

    queries = range(1, 11)
    if args.query != None:
        queries = [args.query]
    for query in queries:
        print("\nQuery {}".format(query))
        if query <= 6:
            print("\nPandas Output")
            df = pandas_queries[query - 1]()
            print(df)
            if store:
                df.to_csv(f"submission/pandas_sol{query}.csv", index=False)
        print("\nSQLite Output")
        df = runSQL(query, store)
        print(df)
