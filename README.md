# Movie Ratings & Genre Trends: A SQL Exploration

Analysis of a movie ratings dataset (MovieLens-style schema) to uncover trends in audience preferences over time — how average ratings shift by release year, which genres rise and fall in popularity, and where audience opinion is most divided.

## Overview

This project uses SQL to answer a few core questions:

- Do average movie ratings trend up, down, or stay flat over time?
- Which genres have grown or declined in popularity (by ratings volume) year over year?
- Which genre is the "top-rated" genre in a given year, and does that leader change over time?
- Which movies are most polarizing — high rating volume but high disagreement among raters?
- Are there seasonal patterns in when people rate movies?

## Dataset

- Source: [MovieLens dataset](https://grouplens.org/datasets/movielens/) *(update with the specific version/size you used, e.g. ml-25m)*
- Tables used:
  - `movies(movie_id, title, release_year, genres)`
  - `ratings(rating_id, user_id, movie_id, rating, rating_timestamp)`
- Genres were originally stored as a pipe-delimited string (e.g. `Action|Comedy`) and normalized into a `movie_genres(movie_id, genre)` bridge table to support per-genre aggregation.

## Tech Stack

- SQL (PostgreSQL) *(swap in your actual engine — MySQL, SQLite, BigQuery, etc.)*
- [Optional: Python/pandas + matplotlib for visualizing query outputs]

## Key Queries

| File | Description |
|---|---|
| `01_schema_setup.sql` | Creates tables and normalizes genres into a bridge table |
| `02_rating_trends_by_year.sql` | Average rating and volume by release year |
| `03_genre_popularity_by_year.sql` | Ratings volume and average rating per genre per year |
| `04_genre_yoy_change.sql` | Year-over-year rating change per genre using `LAG()` |
| `05_top_genre_per_year.sql` | Highest-rated genre each year using `RANK()` |
| `06_polarizing_movies.sql` | Movies with highest rating variance (`STDDEV`) |
| `07_seasonal_patterns.sql` | Rating volume/average by month |

## Key Findings

*(Fill these in with your actual results — this section is what recruiters and interviewers will actually read.)*

- Example: "Average ratings for [genre] declined by X points between 2005–2020, while [genre] grew steadily in both volume and average score."
- Example: "The most polarizing movies tend to cluster in [genre] — high variance suggests a niche but passionate audience."
- Example: "Ratings volume spikes in [month/season], suggesting [hypothesis]."

## What I'd Explore Next

- Correlate genre trends with external events (e.g., streaming platform launches, major franchise releases)
- Segment trends by user cohort instead of aggregate averages
- Build a lightweight dashboard (Python/Tableau) on top of these queries

## How to Run

1. Load the dataset into your SQL engine of choice.
2. Run `01_schema_setup.sql` to normalize the genre column.
3. Run the numbered query files in order, or individually to explore specific questions.

---

*Built as a portfolio project to demonstrate SQL fluency — joins, aggregations, and window functions (`LAG`, `RANK`, `STDDEV`) — applied to a real-world dataset.*
