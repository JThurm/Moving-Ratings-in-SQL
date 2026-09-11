# MovieLens Analytics — SQL & Data Analysis

A PostgreSQL and Python data-analysis project exploring how movie ratings, genre popularity, audience disagreement, and rating activity change across more than a century of film releases.

The project uses **PostgreSQL, SQL, Pandas, Plotly, and Streamlit** to transform the MovieLens dataset into a collection of reproducible analyses and an interactive dashboard.

---

## Overview

This project investigates how audience rating behavior changes across time.

Rather than focusing only on average movie ratings, the analysis considers several dimensions of movie reception:

* Rating volume
* Average rating
* Rating variability
* Genre popularity
* Genre polarization
* Historical-era trends
* Seasonal rating activity
* Historical and industry events

The analysis covers **100,818 ratings across 106 release years from 1902–2018**.

---

## Key Questions

The project asks:

* Do average movie ratings trend upward or downward over time?
* Which genres receive the most rating activity?
* Are the most popular genres also the highest-rated?
* How does genre activity change across historical eras?
* Which genres produce the most disagreement?
* Which movies are the most polarizing?
* Does rating volume relate to average rating or variability?
* Does audience disagreement change over time?
* Are there meaningful seasonal patterns in rating activity?
* How do major historical and industry events align with genre trends?

---

## Key Findings

### Popularity ≠ Rating Quality

Drama has the largest rating volume at approximately **41,926 ratings**, while Film-Noir has the highest average rating among qualifying genres at approximately **3.92**.

This demonstrates that the most frequently rated genres are not necessarily the highest-rated.

### Genre Preferences Change

Genre activity shifts considerably across historical periods. Drama remains consistently important, while Action, Adventure, Sci-Fi, Horror, and Fantasy become more prominent in later periods.

### Some Genres Are More Polarizing

Horror has the highest rating standard deviation among genres with at least 100 ratings, at approximately **1.14**.

Higher variability indicates greater disagreement rather than lower quality.

### Popularity Has Little Relationship with Polarization

At the movie level, the correlation between rating volume and rating variability is approximately:

```text
-0.058
```

This is an extremely weak relationship, suggesting that highly rated movies are not automatically more or less polarizing because they receive more ratings.

### Average Rating and Variability

The correlation between average rating and rating variability is approximately:

```text
-0.423
```

This indicates a moderate negative relationship: movies with higher average ratings tend to show somewhat lower rating variability.

### Seasonal Activity Is Uneven

The dataset contains several large rating spikes, including:

* May 2017 — 2,397 ratings
* August 2000 — 2,319 ratings
* November 2015 — 1,839 ratings
* April 2016 — 1,755 ratings

However, the spikes are not consistent enough across years to establish a strong recurring seasonal pattern.

---

# Interactive Dashboard

The project includes a Streamlit dashboard designed to present the analysis in two levels:

```text
Overview
   ↓
Findings
   ↓
Explore Data
   ↓
Methodology
```

### Overview

Provides a high-level introduction to the dataset and broad rating trends.

### Findings

Presents the major conclusions from the SQL analysis in a guided format.

### Explore Data

Provides interactive visualizations for:

* Rating trends
* Genre popularity
* Genre changes
* Historical eras
* Audience polarization
* Rating variability
* Seasonal patterns
* Historical events

### Methodology

Documents:

* Database structure
* Analytical methods
* SQL queries
* Statistical measures
* Data limitations
* Reproducibility

---

# Project Structure

```text
Moving-Ratings-in-SQL/
│
├── data/
│   └── ml-latest-small/
│       ├── movies.csv
│       ├── ratings.csv
│       ├── tags.csv
│       └── links.csv
│
├── sql/
│   ├── 01_schema_setup.sql
│   ├── 02_load_data.sql
│   ├── 03_normalizing_genres.sql
│   ├── 04_add_release_year.sql
│   ├── 05_rating_trends_by_year.sql
│   ├── 06_genre_popularity_by_year.sql
│   ├── 07_genre_yoy_change.sql
│   ├── 08_top_genre_per_year.sql
│   ├── 09_polarizing_movies.sql
│   ├── 10_seasonal_patterns.sql
│   ├── 11_historical_era_genres.sql
│   ├── 12_genre_popularity_vs_rating.sql
│   ├── 13_rating_disagreement_over_time.sql
│   ├── 14_genre_polarization.sql
│   ├── 15_rating_volume_vs_variability.sql
│   └── 16_historical_events.sql
│
├── results/
│   ├── 01_rating_trends_by_year.csv
│   ├── 02_genre_popularity_by_year.csv
│   ├── 03_genre_yoy_change.csv
│   ├── 04_top_genre_per_year.csv
│   ├── 05_polarizing_movies.csv
│   ├── 06_seasonal_patterns.csv
│   ├── 07_historical_era_genres.csv
│   ├── 08_genre_popularity_vs_rating.csv
│   ├── 09_rating_disagreement_over_time.csv
│   ├── 10_genre_polarization.csv
│   ├── 11_rating_volume_vs_variability.csv
│   └── 12_historical_events.csv
│
├── dashboard/
│   └── app.py
│
├── findings.md
├── requirements.txt
└── README.md
```

---

# Database Design

The original MovieLens dataset stores genres as a pipe-delimited string:

```text
Action|Comedy|Sci-Fi
```

The project normalizes this structure into a bridge table:

```text
movie_genres
----------------
movie_id
genre
```

This allows individual genres to be analyzed independently.

The core relational structure is:

```text
movies
 ├── movie_id
 ├── title
 ├── release_year
 └── genres

ratings
 ├── rating_id
 ├── user_id
 ├── movie_id
 ├── rating
 └── rating_timestamp

movie_genres
 ├── movie_id
 └── genre
```

---

# SQL Analysis

The project contains 12 analytical queries.

| Query                                  | Purpose                                          |
| -------------------------------------- | ------------------------------------------------ |
| `05_rating_trends_by_year.sql`         | Average rating and rating volume by release year |
| `06_genre_popularity_by_year.sql`      | Genre rating activity by year                    |
| `07_genre_yoy_change.sql`              | Genre rating changes using `LAG()`               |
| `08_top_genre_per_year.sql`            | Highest-rated genre using `RANK()`               |
| `09_polarizing_movies.sql`             | Most polarizing movies using `STDDEV()`          |
| `10_seasonal_patterns.sql`             | Rating activity by month                         |
| `11_historical_era_genres.sql`         | Genre trends across historical eras              |
| `12_genre_popularity_vs_rating.sql`    | Popularity vs. average rating                    |
| `13_rating_disagreement_over_time.sql` | Rating disagreement by year                      |
| `14_genre_polarization.sql`            | Genre-level rating variability                   |
| `15_rating_volume_vs_variability.sql`  | Rating volume, quality, and variability          |
| `16_historical_events.sql`             | Genre activity around historical/industry events |

---

# Technologies

### Database

* PostgreSQL
* SQL
* Relational data modeling

### Analysis

* Aggregate functions
* `JOIN`
* `GROUP BY`
* `LAG()`
* `RANK()`
* `STDDEV()`
* `CORR()`

### Visualization

* Python
* Pandas
* Plotly
* Streamlit

---

# Running the Project

## 1. Load the Database

Create the database schema using:

```text
sql/01_schema_setup.sql
```

Load the MovieLens data using:

```text
sql/02_load_data.sql
```

Normalize the movie genres using:

```text
sql/03_normalizing_genres.sql
```

Prepare the release-year field using:

```text
sql/04_add_release_year.sql
```

---

## 2. Run the Analysis

Run the analytical SQL files in `sql/`.

The results can be exported into the `results/` directory as CSV files.

The dashboard expects the result files to follow this naming convention:

```text
01_rating_trends_by_year.csv
02_genre_popularity_by_year.csv
03_genre_yoy_change.csv
...
12_historical_events.csv
```

---

# Running the Dashboard

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

Then launch Streamlit from the project root:

```bash
streamlit run dashboard/app.py
```

The dashboard will load the exported CSV files from:

```text
results/
```

---

# Important Limitations

The analysis should be interpreted with several limitations in mind.

### Rating Volume

Rating volume represents submitted ratings, not unique viewers, movie production volume, box-office performance, or streaming views.

### Uneven Samples

The dataset contains substantially more rating activity for recent movies than older films. Early-year averages can therefore be much less reliable.

### Genre Assignment

Movies can belong to multiple genres, so a movie's ratings can contribute to more than one genre.

### Missing Genres

`(no genres listed)` represents missing genre information rather than an actual genre.

### Year-over-Year Analysis

The `LAG()` analysis compares each genre with its previous available observation. Missing years can therefore make some reported changes span multiple calendar years.

### Correlation

Correlation measures statistical association, not causation.

### Historical Events

Historical and industry events are included as contextual markers. The analysis does not establish that these events caused changes in movie ratings or genre popularity.

---

# Documentation

The detailed analytical interpretation is available in:

```text
findings.md
```

The findings report provides:

* Executive summary
* Research questions
* Methodology
* Detailed findings
* Statistical interpretation
* Historical context
* Data-quality discussion
* Limitations
* Future work

---

# Project Goal

This project was built as a portfolio demonstration of practical SQL and data-analysis skills.

Rather than simply querying a database for individual answers, the project demonstrates an end-to-end workflow:

```text
Raw Data
   ↓
Relational Modeling
   ↓
SQL Analysis
   ↓
Statistical Interpretation
   ↓
CSV Results
   ↓
Python Visualization
   ↓
Interactive Dashboard
```

The goal is to demonstrate the ability to take a real-world dataset, structure it for analysis, formulate meaningful questions, perform reproducible SQL analysis, interpret the results critically, and communicate those results through an interactive application.
