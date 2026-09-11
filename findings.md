# MovieLens Analytics — Findings Report

## 1. Executive Summary

This report presents the findings from a PostgreSQL-based analysis of the MovieLens `ml-latest-small` dataset. The analysis examines how movie ratings, genre popularity, audience disagreement, and rating activity vary across more than a century of film releases.

The dataset contains **100,818 ratings across 106 release years, spanning 1902–2018**. The analysis combines relational modeling, aggregations, joins, window functions, and statistical measures such as standard deviation and correlation.

Several major patterns emerged:

* **Rating averages fluctuate over time without a strong long-term upward or downward trend.**
* **Drama and Comedy dominate rating volume**, but the most popular genres are not necessarily the highest-rated.
* **Genre preferences shift substantially across historical eras.**
* **Audience disagreement varies by year and genre**, with Horror showing the highest genre-level rating variability among genres with at least 100 ratings.
* **Movie popularity has only a very weak relationship with rating variability**, while rating volume has a moderate positive relationship with average rating.
* **Some highly rated movies are also highly polarizing**, demonstrating that average rating alone does not capture audience consensus.
* **Rating activity contains large monthly spikes**, but the available data does not support a strong recurring seasonal pattern.
* Historical and industry events provide useful context for some changes in genre activity, but the analysis cannot establish causal relationships.

The goal of this project is therefore not simply to identify which movies or genres are "best," but to examine how audience rating behavior changes across time and how different measures of popularity, quality, and disagreement interact.

---

# 2. Research Questions

The analysis was designed around the following questions:

1. How do average movie ratings change across release years?
2. Which genres receive the most rating activity?
3. Are the most popular genres also the highest-rated?
4. How volatile are genre ratings from year to year?
5. Does the highest-rated genre change across different periods?
6. Which movies generate the greatest disagreement among viewers?
7. Does rating disagreement change over time?
8. Which genres consistently produce more polarized audiences?
9. Is rating volume related to average rating or rating variability?
10. Are there noticeable patterns in when users submit ratings?
11. How do genre trends compare across major historical eras?
12. Do major historical or industry events coincide with changes in genre activity?

---

# 3. Data & Methodology

## 3.1 Dataset

The project uses the MovieLens `ml-latest-small` dataset provided by GroupLens.

The primary source tables are:

```text
movies
ratings
```

The original movie data stores multiple genres in a single pipe-delimited field. For example:

```text
Action|Comedy
```

To make genre-level analysis easier, the project normalizes these values into a separate bridge table:

```text
movie_genres(movie_id, genre)
```

This allows individual genres to be grouped and analyzed independently.

---

## 3.2 Analytical Pipeline

The project follows this general pipeline:

```text
MovieLens CSV Files
        │
        ▼
    PostgreSQL
        │
        ├── movies
        ├── ratings
        └── movie_genres
        │
        ▼
   SQL Analysis
        │
        ▼
    CSV Results
        │
        ▼
 Python / Pandas
        │
        ▼
 Streamlit / Plotly
```

The SQL queries perform the primary data aggregation and analysis. Python and Streamlit are then used to present the results through an interactive dashboard.

---

## 3.3 Analytical Measures

### Average Rating

The arithmetic mean of submitted ratings within the selected grouping.

### Rating Volume

The number of submitted ratings associated with a movie, genre, or release year.

Rating volume is treated as a measure of **rating activity**, not as a direct measurement of movie production or unique viewers.

### Rating Variability

Rating variability is measured using standard deviation:

```text
STDDEV(rating)
```

A higher standard deviation indicates that individual ratings are more spread out and therefore represent greater disagreement among users.

### Genre Popularity

Genre popularity is measured using rating volume. Genres with more submitted ratings are considered more popular within the MovieLens rating activity represented by this dataset.

### Correlation

Pearson correlation coefficients are used in the movie-level analysis to examine relationships between:

* rating volume and rating variability
* rating volume and average rating
* average rating and rating variability

---

# 4. Findings

## 4.1 Rating Trends Over Time

**SQL:** `sql/05_rating_trends_by_year.sql`

Average movie ratings fluctuate considerably across release years, but the overall data does not show a strong, consistent upward or downward trend.

Ratings are relatively variable during the earliest years, become more stable across much of the middle of the dataset, and generally decline from the late 1970s into the 1990s. Average ratings then remain relatively stable through much of the 2000s and 2010s.

Individual years should not automatically be interpreted as changes in overall movie quality. The number of ratings supporting each year's average is an important consideration.

### Sample Size Matters

Early release years frequently contain very small numbers of ratings. For example, some years contain only one or a handful of observations.

A year with one rating can produce an average of 4.50, but that value provides very little evidence about the broader quality of movies released that year.

By comparison, years such as 1994 contain thousands of ratings and therefore provide substantially stronger evidence about the rating behavior represented in the dataset.

The most recent years can also have smaller samples. Therefore, both ends of the dataset require more caution than years with substantial rating volume.

### Key takeaway

> **The apparent movement of average ratings over time is strongly influenced by differences in sample size, so rating averages should be interpreted alongside rating volume.**

---

# 4.2 Genre Popularity Across Time

**SQL:** `sql/06_genre_popularity_by_year.sql`

Drama and Comedy are among the most consistently represented genres in the early portion of the dataset.

From 1900–1950:

| Genre    | Years Represented |
| -------- | ----------------: |
| Comedy   |                33 |
| Drama    |                31 |
| Romance  |                28 |
| Musical  |                22 |
| Crime    |                21 |
| War      |                20 |
| Thriller |                20 |
| Fantasy  |                20 |

Drama also shows substantial growth in rating volume during the early decades:

* 1920s: 56 ratings
* 1930s: 355 ratings
* 1940s: 669 ratings

Romance, Musical, Children, and Film-Noir also become more prominent during the 1930s and 1940s.

### Interpretation

The results are consistent with a broader shift in the types of films represented and rated during different periods. Historical developments such as the transition from silent film to sound and the social conditions surrounding the Great Depression and World War II provide useful context.

However, these relationships should not be interpreted as causal. The dataset does not contain information about audience motivations, economic conditions, production decisions, or other factors necessary to establish causation.

### Key takeaway

> **Genre representation changes substantially over time, while Drama, Comedy, and Romance remain important recurring genres throughout early cinema.**

---

# 4.3 Year-over-Year Genre Change

**SQL:** `sql/07_genre_yoy_change.sql`

The year-over-year analysis uses the SQL `LAG()` window function to compare a genre's average rating with its previous available observation.

Musicals show some of the largest observed changes in the early portion of the dataset, including:

* A **3.13-point decrease** in 1931
* A **2.79-point increase** in 1933

Other large changes occur in genres including Comedy, Adventure, Horror, Drama, and Fantasy.

### Important limitation

These should not always be interpreted as literal year-to-year changes.

If a genre has no observations for one or more years, `LAG()` compares the current observation with the previous **available** observation. Consequently, a reported "year-over-year" difference may span multiple calendar years.

Small samples can also produce large swings in average rating.

### Key takeaway

> **Large year-over-year changes often reflect both genuine variation and the instability caused by sparse observations.**

---

# 4.4 Top Genre by Year

**SQL:** `sql/08_top_genre_per_year.sql`

The highest-rated genre does not remain consistent across the dataset.

The early period provides several examples of this movement:

* Musical and Fantasy appear among the highest-rated genres in the late 1930s.
* Romance ranks first in 1940, 1942, and 1946.
* Film-Noir ranks first in 1941.
* Drama becomes the top genre in 1948 and 1950.

The results indicate that there is no single genre that consistently dominates average rating across all periods.

The later dataset also contains a greater representation of genres such as Action, Adventure, Sci-Fi, Horror, and Fantasy.

### Key takeaway

> **The genre receiving the highest average rating changes over time, suggesting that audience preferences and highly rated film categories are not static.**

---

# 4.5 Popularity vs. Average Rating

**SQL:** `sql/12_genre_popularity_vs_rating.sql`

One of the clearest findings from the expanded analysis is that **rating volume and average rating measure different things**.

Among genres with at least 100 ratings:

| Genre     | Rating Volume | Average Rating |
| --------- | ------------: | -------------: |
| Drama     |        41,926 |           3.66 |
| Comedy    |        39,053 |           3.38 |
| Action    |        30,631 |           3.45 |
| Thriller  |        26,447 |           3.49 |
| Adventure |        24,161 |           3.51 |
| Romance   |        18,124 |           3.51 |
| Sci-Fi    |        17,237 |           3.46 |

Drama has the largest rating volume and also has a relatively high average rating, but it is not the highest-rated genre.

The highest average ratings are found in genres with substantially lower rating volumes:

| Genre       | Rating Volume | Average Rating |
| ----------- | ------------: | -------------: |
| Film-Noir   |           870 |           3.92 |
| War         |         4,859 |           3.81 |
| Documentary |         1,219 |           3.80 |
| Crime       |        16,681 |           3.66 |
| Drama       |        41,926 |           3.66 |

Film-Noir, for example, ranks first by average rating while ranking near the bottom in overall rating volume.

### Key takeaway

> **The genres receiving the most rating activity are not necessarily the genres receiving the highest ratings.**

This is one of the reasons the dashboard separates **popularity** from **rating quality** rather than treating them as the same measurement.

---

# 4.6 Genre Trends Across Historical Eras

**SQL:** `sql/11_historical_era_genres.sql`

To examine broader historical patterns, the dataset was divided into seven eras:

| Era               | Years     |
| ----------------- | --------- |
| Early Cinema      | 1900–1929 |
| Depression & WWII | 1930–1945 |
| Postwar Cinema    | 1946–1959 |
| New Hollywood     | 1960–1979 |
| Blockbuster Era   | 1980–1999 |
| Early Digital     | 2000–2006 |
| Streaming Era     | 2007–2018 |

Drama is the largest genre by rating volume in most early and modern periods.

The Blockbuster Era is notable for the large increase in rating activity associated with Comedy, Drama, Action, and Thriller. During the Early Digital and Streaming eras, Drama remains highly represented while Action, Adventure, and Thriller continue to account for substantial rating activity.

### Era-level rating volume

| Historical Era    | Ratings |
| ----------------- | ------: |
| Early Cinema      |     141 |
| Depression & WWII |   1,446 |
| Postwar Cinema    |   2,125 |
| New Hollywood     |   7,851 |
| Blockbuster Era   |  49,992 |
| Early Digital     |  23,441 |
| Streaming Era     |  15,785 |

The dramatic increase in later-era rating volume means that comparisons across eras should be interpreted with sample size in mind.

### Key takeaway

> **Genre activity shifts substantially across historical periods, but the dataset becomes much denser in later eras, making modern-period patterns more statistically informative.**

---

# 4.7 Rating Disagreement Over Time

**SQL:** `sql/13_rating_disagreement_over_time.sql`

Average rating describes the center of the rating distribution, but it does not show whether viewers agree.

To address this, rating standard deviation was calculated for each release year.

The results show meaningful variation in disagreement across years. Among years with at least 20 ratings, several years exhibit particularly high variability:

| Release Year | Ratings | Average Rating | Std. Dev. |
| ------------ | ------: | -------------: | --------: |
| 1928         |      23 |           3.17 |      1.35 |
| 2018         |     269 |           3.47 |      1.12 |
| 2017         |   1,107 |           3.55 |      1.12 |
| 1999         |  11,660 |           3.53 |      1.11 |
| 2015         |   3,003 |           3.44 |      1.11 |

The 1928 result demonstrates the importance of sample size: its high standard deviation is based on only 23 ratings.

The high variability observed in several modern years is more meaningful because those years contain substantially larger rating samples.

### Key takeaway

> **Audience disagreement varies across release years, but the reliability of that measurement depends heavily on the number of ratings available.**

---

# 4.8 Genre Polarization

**SQL:** `sql/14_genre_polarization.sql`

Genre-level polarization was measured using rating standard deviation, with a minimum threshold of 100 ratings.

The genres with the highest observed rating variability include:

| Genre     | Ratings | Average Rating | Std. Dev. |
| --------- | ------: | -------------: | --------: |
| Horror    |   7,291 |           3.26 |      1.14 |
| Comedy    |  39,053 |           3.38 |      1.07 |
| Sci-Fi    |  17,237 |           3.46 |      1.07 |
| Children  |   9,208 |           3.41 |      1.06 |
| Action    |  30,631 |           3.45 |      1.05 |
| Fantasy   |  11,834 |           3.49 |      1.04 |
| Adventure |  24,161 |           3.51 |      1.03 |
| Thriller  |  26,447 |           3.49 |      1.03 |

Horror has the highest standard deviation among the qualifying genres.

Interestingly, polarization does not mean that a genre or movie is necessarily poorly rated. It simply means that ratings are more spread out.

### Key takeaway

> **A polarized audience and a low-rated audience are not the same thing. Standard deviation measures disagreement, not quality.**

---

# 4.9 Most Polarizing Movies

**SQL:** `sql/09_polarizing_movies.sql`

The movie-level polarization analysis identifies films with at least 100 ratings and ranks them by rating standard deviation.

Several recognizable films show substantial disagreement:

| Movie                                     | Ratings | Average | Std. Dev. |
| ----------------------------------------- | ------: | ------: | --------: |
| Austin Powers: The Spy Who Shagged Me     |     121 |    3.20 |      1.22 |
| The Big Lebowski                          |     106 |    3.92 |      1.14 |
| Star Wars: Episode I - The Phantom Menace |     140 |    3.11 |      1.12 |
| Dumb & Dumber                             |     133 |    3.06 |      1.12 |
| Four Weddings and a Funeral               |     103 |    3.52 |      1.11 |
| 2001: A Space Odyssey                     |     109 |    3.89 |      1.10 |

The most interesting examples are movies such as **The Big Lebowski** and **2001: A Space Odyssey**.

Both have relatively high average ratings while still exhibiting significant disagreement.

This demonstrates why average rating alone can be misleading. A movie can be highly regarded overall while still generating strong differences of opinion.

### Key takeaway

> **Highly polarizing movies are not necessarily poorly received; they can instead produce unusually strong and divided reactions.**

---

# 4.10 Rating Volume vs. Variability

**SQL:** `sql/15_rating_volume_vs_variability.sql`

The movie-level analysis examines relationships among rating volume, average rating, and rating variability for movies with at least 20 ratings.

The resulting Pearson correlations are:

| Relationship                   | Correlation |
| ------------------------------ | ----------: |
| Rating Volume ↔ Variability    |      -0.058 |
| Rating Volume ↔ Average Rating |       0.303 |
| Average Rating ↔ Variability   |      -0.423 |

### Rating Volume vs. Variability

The correlation of **-0.058** is extremely weak.

This suggests that the number of ratings a movie receives has almost no linear relationship with how much disagreement exists among its viewers.

In other words, highly rated movies are not automatically more or less polarizing simply because they have more ratings.

### Rating Volume vs. Average Rating

The correlation of **0.303** indicates a moderate positive relationship.

Movies with more ratings tend to have somewhat higher average ratings in this dataset, although the relationship is not strong enough to imply that popularity determines quality.

### Average Rating vs. Variability

The correlation of **-0.423** is stronger and negative.

This suggests that movies with higher average ratings tend to have somewhat lower rating variability.

However, the relationship is still not deterministic. Individual highly rated movies can remain strongly polarizing.

### Key takeaway

> **Popularity has little relationship with disagreement, while higher average ratings show a moderate tendency to be associated with more consistent ratings.**

---

# 4.11 Seasonal Rating Activity

**SQL:** `sql/10_seasonal_patterns.sql`

Rating activity varies considerably across months and years.

Several of the largest observed monthly spikes include:

| Month         | Ratings |
| ------------- | ------: |
| May 2017      |   2,397 |
| August 2000   |   2,319 |
| November 2015 |   1,839 |
| April 2016    |   1,755 |

However, these spikes are not consistent enough across years to establish a strong recurring seasonal pattern.

For example:

* August 2000: 2,319 ratings
* August 2003: 108 ratings

This large difference suggests that the observed variation may be influenced by when users submitted ratings, the composition of the dataset, or other collection effects rather than a simple recurring seasonal cycle.

Some months also contain extremely small samples. For example, October 1997 contains only one rating, making any calculated average for that month unreliable.

### Key takeaway

> **The data contains noticeable monthly spikes, but not enough consistency to conclude that rating activity follows a strong seasonal pattern.**

---

# 4.12 Historical and Industry Events

**SQL:** `sql/16_historical_events.sql`

The final analysis places genre activity alongside selected historical and industry events.

The events examined include:

* Great Depression — 1929–1939
* World War II — 1939–1945
* Star Wars release — 1977
* Jurassic Park release — 1993
* The Lord of the Rings trilogy — 2001–2003
* Netflix begins streaming — 2007
* Iron Man / MCU launch — 2008
* Instagram launch — 2010
* Major streaming expansion — 2015

These event markers are intended as **contextual reference points rather than causal variables**.

### Great Depression

Between 1929 and 1939, Drama has the largest rating volume among genres represented in the event window.

Musical, Romance, Fantasy, and Comedy also show substantial activity.

The period is historically interesting because it overlaps with major changes in both society and the film industry, but the dataset alone cannot determine whether economic conditions caused changes in audience preferences.

### World War II

During 1939–1945, Drama has the largest rating volume, followed by Romance, Children, Musical, and Fantasy.

The period also overlaps with the increased prominence of Film-Noir observed in the broader genre analysis.

Again, these patterns are **consistent with historical context**, but they should not be presented as evidence that World War II caused the changes.

### Star Wars — 1977

The 1977 event window shows particularly strong rating activity for:

* Adventure
* Sci-Fi
* Action

Sci-Fi has an average rating of approximately **4.12** during the year, while Action averages approximately **4.10**.

This provides an interesting contextual snapshot around one of the most influential franchise releases of the period.

### The Lord of the Rings — 2001–2003

During the trilogy's release period, Drama, Comedy, Action, Adventure, and Thriller account for substantial rating activity.

The dataset shows substantial rating volume during this period, although the analysis cannot isolate the effect of the trilogy itself from broader changes in movie popularity and rating behavior.

### Streaming Expansion

The 2007 Netflix streaming marker and 2015 streaming expansion provide reference points for the increasing importance of digital distribution.

Drama remains the largest genre by rating volume in 2007 and 2008, while Action and Adventure also represent substantial activity.

These results are useful for contextual exploration but should not be interpreted as proof that streaming caused a particular genre to become more popular.

### Key takeaway

> **Historical and industry events provide useful context for interpreting changes in genre activity, but the available data supports correlation and comparison—not causal inference.**

---

# 5. Overall Conclusions

Several broad conclusions emerge when the analyses are considered together.

### 1. Popularity and quality are different measurements

Drama receives the largest number of ratings, but Film-Noir, War, and Documentary have higher average ratings.

This demonstrates why a single metric is insufficient for understanding audience behavior.

### 2. Genre preferences change over time

The genres receiving the greatest rating activity vary across historical eras. Later periods contain substantially more activity in Action, Adventure, Sci-Fi, Horror, and Fantasy than the earliest periods.

### 3. Audience disagreement is an important dimension of movie reception

Average rating does not tell the complete story. Standard deviation reveals movies and genres where viewers disagree more strongly.

### 4. Popularity does not strongly predict polarization

The movie-level correlation between rating volume and rating variability is approximately **-0.058**, indicating almost no linear relationship.

A movie can therefore be extremely popular without being particularly polarizing.

### 5. Sample size is one of the most important limitations

The dataset becomes dramatically denser in later decades. Early observations can therefore appear unusually high or low simply because they are based on small numbers of ratings.

### 6. Historical context is useful, but causation cannot be established

Historical and industry events provide useful reference points for interpreting changes in genre activity, but the dataset does not contain enough variables to determine why those changes occurred.

---

# 6. Data Quality & Limitations

The following limitations should be considered throughout the analysis.

### Uneven temporal coverage

The dataset contains substantially more ratings for recent movies than older films. Comparisons across centuries and eras should therefore account for sample size.

### Small samples

Some early years and individual genre-year combinations contain very few ratings. Their averages and standard deviations may be unstable.

### Rating volume is not movie popularity

`rating_count` represents the number of submitted ratings. It does not represent:

* unique viewers
* box-office performance
* total movie production
* streaming views

### Multi-genre movies

Movies can belong to multiple genres. Their ratings therefore contribute to each assigned genre.

### Missing genres

`(no genres listed)` represents missing genre information and is excluded from several genre-specific analyses.

### Year-over-year gaps

The `LAG()` analysis compares each genre with its previous available observation. Missing years can therefore make some "year-over-year" changes span more than one calendar year.

### Correlation is not causation

The correlation analyses identify linear relationships but do not demonstrate causal mechanisms.

### Historical event analysis

Historical and industry events are contextual markers. They are not controlled experiments and should not be interpreted as proof that an event caused a change in rating behavior.

---

# 7. Reproducibility

The project separates the SQL analysis from the visualization layer.

The SQL queries are located in:

```text
sql/
```

The exported analytical results are stored in:

```text
results/
```

The interactive dashboard is located in:

```text
dashboard/app.py
```

The dashboard consumes the exported CSV results rather than performing the primary analytical calculations itself.

This separation makes the project easier to inspect and reproduce:

```text
SQL → Results → Visualization
```

---

# 8. Analysis Inventory

| SQL Query                              | Analysis                                       |
| -------------------------------------- | ---------------------------------------------- |
| `05_rating_trends_by_year.sql`         | Rating trends by release year                  |
| `06_genre_popularity_by_year.sql`      | Genre popularity by year                       |
| `07_genre_yoy_change.sql`              | Year-over-year genre changes                   |
| `08_top_genre_per_year.sql`            | Highest-rated genre by year                    |
| `09_polarizing_movies.sql`             | Most polarizing movies                         |
| `10_seasonal_patterns.sql`             | Seasonal rating activity                       |
| `11_historical_era_genres.sql`         | Genre trends across historical eras            |
| `12_genre_popularity_vs_rating.sql`    | Genre popularity vs. average rating            |
| `13_rating_disagreement_over_time.sql` | Rating disagreement by release year            |
| `14_genre_polarization.sql`            | Genre-level polarization                       |
| `15_rating_volume_vs_variability.sql`  | Rating volume, average rating, and variability |
| `16_historical_events.sql`             | Genre trends around historical/industry events |

---

# 9. Future Work

Potential extensions to this project include:

1. Normalize and analyze rating timestamps based on user activity rather than movie release year.
2. Add confidence intervals or minimum sample thresholds to reduce the influence of sparse observations.
3. Compare genre trends using proportions rather than raw rating counts to better account for changes in overall dataset volume.
4. Investigate whether rating distributions become more or less polarized across decades.
5. Analyze individual users to determine whether different groups of users exhibit different genre preferences.
6. Compare MovieLens results with external box-office or streaming datasets.
7. Build statistical models that control for release year, genre, rating volume, and other variables simultaneously.
8. Improve the historical event analysis with more systematically selected events and pre/post-event comparisons.

---

# 10. Final Takeaway

The central lesson from this project is that movie ratings are more complicated than a single average score.

Rating volume, average rating, variability, genre, release period, and audience activity each describe a different aspect of the dataset. Looking at these measurements together reveals patterns that would be missed by simply ranking movies by average score.

The analysis therefore demonstrates how SQL can be used not only to retrieve information, but to transform a relatively simple ratings dataset into a structured investigation of **audience behavior, genre evolution, and changing patterns in movie reception**.
