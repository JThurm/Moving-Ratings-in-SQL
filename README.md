# Movie Ratings & Genre Trends: A SQL Exploration

A SQL-based analysis of a MovieLens-style movie ratings dataset exploring how audience ratings and genre popularity change over time. The project uses relational modeling, aggregations, joins, and window functions to investigate rating trends, genre popularity, audience disagreement, and rating activity.

## Overview

This project uses PostgreSQL and SQL analytics to answer several questions about movie ratings and audience behavior:

* Do average movie ratings trend upward, downward, or remain relatively stable over time?
* Which genres appear most consistently across different periods?
* Which genres grow or decline in popularity based on rating volume?
* Which genre is the highest-rated in a given year, and does that leader change over time?
* Which movies are the most polarizing among viewers?
* Are there noticeable patterns in when users submit ratings?

## Dataset

* **Source:** [MovieLens dataset](https://grouplens.org/datasets/movielens/)
* **Schema:**

  * `movies(movie_id, title, release_year, genres)`
  * `ratings(rating_id, user_id, movie_id, rating, rating_timestamp)`
* The original `genres` column stores multiple genres as a pipe-delimited string, such as `Action|Comedy`.
* Genres were normalized into a separate `movie_genres(movie_id, genre)` bridge table, allowing individual genres to be queried and aggregated independently.

## Tech Stack

* PostgreSQL
* SQL
* Relational database design
* Aggregate functions
* JOINs
* Window functions

## SQL Queries

| File                              | Description                                                           |
| --------------------------------- | --------------------------------------------------------------------- |
| `01_schema_setup.sql`             | Creates the database tables and initial schema                        |
| `02_load_data.sql`                | Loads movie and rating CSV data                                       |
| `03_normalizing_genres.sql`       | Normalizes pipe-delimited genres into the `movie_genres` bridge table |
| `04_add_release_year.sql`         | Converts the extracted release year into an integer                   |
| `05_rating_trends_by_year.sql`    | Analyzes average rating and rating volume by release year             |
| `06_genre_popularity_by_year.sql` | Analyzes rating volume and average rating by genre and year           |
| `07_genre_yoy_change.sql`         | Calculates changes in genre ratings using `LAG()`                     |
| `08_top_genre_per_year.sql`       | Identifies the highest-rated genre each year using `RANK()`           |
| `09_polarizing_movies.sql`        | Identifies movies with high rating disagreement using `STDDEV()`      |
| `10_seasonal_patterns.sql`        | Examines rating activity and averages by month                        |

# Findings

## 1. Rating Trends by Year

**Query:** `sql/05_rating_trends_by_year.sql`

Average ratings fluctuate considerably across release years, but there is no strong overall upward or downward trend. Ratings are relatively variable during the earliest years, become more stable through the middle decades, and generally decline from the late 1970s into the 1990s. From the 2000s through the 2010s, average ratings remain relatively stable around 3.4–3.6.

Individual years can show substantial differences, but these differences should not automatically be interpreted as changes in overall movie quality.

### Caveat: Sample Size

The number of ratings behind each yearly average varies significantly. Early years often contain very few ratings; for example, 1917 has only one rating. With such a small sample, a single user's opinion can have a large effect on the average.

The same issue appears in some of the most recent years. In contrast, years such as 1994 contain thousands of ratings, providing substantially stronger evidence of the average rating for that year.

---

## 2. Genre Popularity by Year

**Query:** `sql/06_genre_popularity_by_year.sql`

From 1900–1950, **Drama and Comedy** are among the most consistently represented genres, appearing across 31 and 33 different years respectively. Romance is also consistently represented, while genres such as Documentary, Sci-Fi, Western, and Animation appear less frequently.

In terms of rating volume, **Drama shows one of the clearest increases**, growing from 56 ratings in the 1920s to 355 in the 1930s and 669 in the 1940s. Romance, Musical, Children, and Film-Noir also become substantially more prominent during the 1930s and 1940s.

### Historical Context

These changes can be considered alongside major historical events of the period. The **Great Depression began in 1929**, creating widespread economic hardship throughout the 1930s. During this period, movies offered audiences an accessible form of entertainment and an opportunity for escapism. Comedy, Romance, Musical, Fantasy, and Adventure films could provide audiences with humor, excitement, and imaginative stories that contrasted with the difficulties of everyday life.

The transition from silent films to sound also changed the types of movies that could be produced and helped make dialogue-heavy films and musicals increasingly practical.

World War II (1939–1945) provides another important historical context. War-related films became more prominent, while darker genres such as Film-Noir also increased from 25 ratings in the 1930s to 181 in the 1940s.

These historical events should be treated as **possible explanations rather than direct causes**. The dataset measures movie genres and user ratings, but it does not contain information about economic conditions, audience motivations, or individual movie-going behavior.

### Caveat: Rating Volume vs. Movie Popularity

`rating_count` measures the number of user ratings, not the number of movies produced or the number of people who watched a movie.

Therefore, an increase in rating volume could reflect greater audience interest, more movies being represented, or differences in how frequently users submitted ratings.

---

## 3. Year-over-Year Genre Change

**Query:** `sql/07_genre_yoy_change.sql`

Musicals show some of the most volatile changes in average rating between 1900 and 1950, including a 3.13-point decrease in 1931 followed by a 2.79-point increase in 1933. Other large changes occur in Comedy, Adventure, Horror, Drama, and Fantasy.

However, these results require caution. Some genres have gaps between observations, meaning a comparison labeled as year-over-year may actually span multiple calendar years. Small sample sizes can also cause large changes in average ratings.

---

## 4. Top Genre per Year

**Query:** `sql/08_top_genre_per_year.sql`

The highest-rated genre changes considerably over time rather than remaining dominated by a single genre.

During the late 1930s, Musical and Fantasy appear among the highest-rated genres in the available years. Romance becomes particularly prominent during the early and mid-1940s, ranking first in 1940, 1942, and 1946. Film-Noir ranks first in 1941, while Drama becomes the top genre in 1948 and 1950.

The prominence of Romance and Film-Noir during the 1940s is particularly interesting when considered alongside the social and cultural effects of World War II. However, the dataset cannot establish that the war directly caused these genre preferences.

More broadly, earlier decades are dominated by established genres such as Drama, Comedy, and Romance, while later decades contain greater representation from Action, Adventure, Sci-Fi, Horror, and Fantasy.

---

## 5. Most Polarizing Movies

**Query:** `sql/09_polarizing_movies.sql`

The most polarizing movies in the dataset tend to be recognizable mainstream films, particularly comedies, science-fiction films, action movies, and major blockbusters from the 1980s through the 2000s.

High polarization does not necessarily mean that a movie is poorly rated. Films such as **The Big Lebowski** and **2001: A Space Odyssey** have relatively high average ratings while still showing substantial disagreement among viewers.

This suggests that polarization may be associated with strong audience reactions rather than simply low movie quality. Distinctive humor, unconventional storytelling, unusual visual styles, and strong fan bases can all contribute to viewers having very different opinions.

---

## 6. Seasonal and Time Patterns

**Query:** `sql/10_seasonal_patterns.sql`

Rating activity varies substantially across months and years, with several notable spikes, including:

* May 2017 — 2,397 ratings
* August 2000 — 2,319 ratings
* November 2015 — 1,839 ratings
* April 2016 — 1,755 ratings

However, these high-volume months are not consistent enough across different years to establish a strong seasonal pattern.

For example, August contains 2,319 ratings in 2000 but only 108 in 2003. This suggests that some of the variation may be related to dataset collection patterns, user activity, or incomplete data rather than a recurring seasonal effect.

Factors such as holidays, school breaks, and movie releases could contribute to some fluctuations, but the dataset does not provide enough information to establish these as definitive causes.

---

# Data Quality & Limitations

Several limitations should be considered when interpreting the results:

* The dataset is unevenly distributed across time, with significantly more ratings available in later decades.
* Early years often contain very small samples, making their averages less reliable.
* Some years and genres have missing observations, which can make apparent year-over-year changes larger than they actually are.
* `rating_count` represents user ratings, not the number of movies produced or total movie viewers.
* The `(no genres listed)` category represents missing genre information rather than an actual genre.
* Historical events provide useful context for interpreting trends, but the dataset cannot establish causal relationships between those events and audience behavior.

---

# What I Would Explore Next

Several extensions could build on this analysis:

1. Compare genre trends across major historical eras, from early cinema through the 2000s.
2. Compare genre popularity with average rating to determine whether the most frequently rated genres were also the highest-rated.
3. Analyze whether rating disagreement changes over time.
4. Determine whether certain genres consistently produce more polarized audiences.
5. Investigate the relationship between rating volume, average rating, and rating variability.
6. Correlate genre trends with external events such as major franchise releases and the rise of streaming platforms.
7. Build a lightweight dashboard using Python or Tableau to visualize the results.

---

# How to Run

1. Load the MovieLens dataset into PostgreSQL.
2. Run `01_schema_setup.sql` to create the database schema.
3. Run `02_load_data.sql` to load the movie and rating data.
4. Run `03_normalizing_genres.sql` to create and populate the normalized genre table.
5. Run `04_add_release_year.sql` to prepare the release-year data.
6. Run the numbered analysis queries individually or in sequence.

---

*Built as a portfolio project to demonstrate SQL fluency through relational modeling, JOINs, aggregations, data normalization, and window functions including `LAG()`, `RANK()`, and `STDDEV()`.*
