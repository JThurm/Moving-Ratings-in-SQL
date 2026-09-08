# Findings — Movie Ratings & Genre Trends (1900-2000s)

Notes from running the analysis queries in `sql/`. Each section corresponds to one query file.

## 1. Rating Trends by Year
*(sql/05_rating_trends_by_year.sql)*

**Finding:** 

The average ratings fluctuate across release years, however it doesn't show a strong overall upward or downward trend. Ratings are relatively high and variable in the early years, become more stable from the 1930s through the 1970s, and then generally decline from the late 1970s into the 1990s. From the 2000s through the 2010s, average ratings remain relatively stable around 3.4–3.6. Additionally some years do have higher or lower averages however that doesn't imply there was a drastic change in movie quality.

A major caveat is the number of ratings supporting each year's average. Early years often have very few ratings, such as 1917 with only one rating, making those averages less reliable and more susceptible to random variation. The most recent years also have fewer ratings, particularly 2018 with only 91 ratings, so those averages should be interpreted cautiously. Years with thousands of ratings, such as 1994 with 5,296 ratings, provide much stronger evidence of the overall rating for that year. 


## 2. Genre Popularity by Year
*(sql/06_genre_popularity_by_year.sql)*

**Finding:** 

From 1900–1950, Drama and Comedy are the most consistently represented genres, appearing across 31 and 33 different years respectively. Romance is also relatively consistent, while genres such as Documentary, Sci-Fi, Western, and Animation appear in fewer years. In terms of volume, Drama shows one of the clearest increases, growing from 56 ratings in the 1920s to 355 in the 1930s and 669 in the 1940s. Romance, Musical, Children, and Film-Noir also become substantially more prominent during the 1930s and 1940s.

Historical events may help explain some of these changes. The Great Depression began in 1929, and movies provided an accessible form of entertainment and escapism during a period of economic hardship, potentially contributing to the popularity of genres such as Comedy, Romance, and Musical films during the 1930s. The transition from silent films to sound films also helped make musicals and dialogue-heavy genres more practical and popular. World War II (1939–1945) may have influenced the increased presence of War-related films as well as darker genres such as Film-Noir, which increased from 25 ratings in the 1930s to 181 in the 1940s. However, these historical events should be treated as possible explanations rather than direct causes, since the dataset only shows genre and rating volume and cannot establish causation.

Unfortunately a caveat is that rating_count meausres the number of ratings, not the number of movies or viewers. Therefore, an increase in ratings may reflect both a greater popularity and differences in how many movies or users contributed ratings. Additionally, some genres have very small sample sizes in individual years, making it difficult to draw strong conclusions about short-term changes.

## 3. Year-over-Year Genre Change
*(sql/07_genre_yoy_change.sql)*

**Finding:** 

Musicals had the most volatile changes in average rating between 1900 and 1950, with a 3.13-point decrease in 1931 followed by a 2.79-point increase in 1933. Other large swings occurred in Comedy, Adventure, Horror, Drama, and Fantasy. However, these changes should be interpreted cautiously because the dataset contains gaps between years for some genres, meaning the comparison may span multiple calendar years rather than representing a true year-over-year change. Small sample sizes can also cause large changes in average ratings from one observation to the next.


## 4. Top Genre per Year
*(sql/08_top_genre_per_year.sql)*

**Finding:** 

The top-rated genre changes considerably rather than remaining consistent across the period. In the late 1930s, Musical and Fantasy were the highest-rated genres in the available years, while Romance became particularly prominent during the early and mid-1940s, ranking first in 1940, 1942, and 1946. Film-Noir also ranked first in 1941, while Drama became the top genre in 1948 and 1950. The concentration of Romance and Film-Noir during the 1940s is especially interesting given the social and cultural effects of World War II, although the dataset cannot establish that historical events directly caused these genre preferences.

Earlier decades are dominated by long-established genres such as Drama, Comedy, and Romance, while later decades show greater representation from genres such as Action, Adventure, Sci-Fi, Horror, and Fantasy. The larger number of ratings available from the 1990s through the 2000s makes patterns in these later periods more reliable than patterns from the early years, where some genres have very few observations. Overall, the results suggest that audience preferences and the types of highly rated movies change over time rather than following one consistent genre trend.

## 5. Most Polarizing Movies
*(sql/09_polarizing_movies.sql)*

**Finding:** 

The most polarizing movies in the full dataset tend to be recognizable, mainstream films, particularly comedies, science-fiction films, action films, and major blockbusters from the 1980s through the 2000s. This generally matches intuition because movies with distinctive humor, unusual storytelling, strong fan bases, or ambitious styles can produce very different reactions among viewers. Interestingly, polarization does not necessarily mean a movie is poorly rated. Films such as The Big Lebowski and 2001: A Space Odyssey have relatively high average ratings while still showing substantial disagreement, suggesting that some movies can be widely respected while remaining divisive. The results therefore suggest that strong audience reactions, rather than simply low quality, are a major characteristic of highly polarizing movies.


## 6. Seasonal / Time Patterns
*(sql/10_seasonal_patterns.sql)*

**Finding:** 

Rating activity varies substantially across months and years, with several notable spikes such as May 2017 (2,397 ratings), August 2000 (2,319), November 2015 (1,839), and April 2016 (1,755). However, the high-volume months are not consistent enough across different years to conclude that there is a strong seasonal pattern. For example, August has 2,319 ratings in 2000 but only 108 in 2003, suggesting that the variation may be more related to when ratings were collected or submitted than to a recurring seasonal effect. Some months also have extremely small sample sizes, such as October 1997 with only one rating, making their average ratings unreliable. Overall, the spikes and gaps appear more likely to reflect dataset collection patterns, user activity, or incomplete data than a clear seasonal trend, although factors such as holidays, school breaks, and movie releases could contribute to some fluctuations.


## Data Quality Notes
*(General observations about the dataset itself)*

The dataset becomes much more heavily represented in the later decades, particularly from the 1980s through the 2000s, while the earliest decades contain relatively few ratings and movies. This creates an uneven sample size across time and makes comparisons between early and modern periods less reliable. Some years and genres also have missing observations, which can affect year-over-year calculations and make apparent changes larger than they actually are. The "(no genres listed)" category represents missing genre information rather than a real genre. Additionally, rating count represents the number of user ratings, not the number of movies produced, so higher rating volume should not be interpreted as higher movie production.


## What I'd Explore Next

I would next explore how movie genres changed across major historical eras, from early cinema through the 2000s, while accounting for the large differences in sample size between periods. I would also compare genre popularity with average rating to determine whether the most frequently rated genres were also the highest-rated. Another useful analysis would be to examine whether rating disagreement changes over time and whether certain genres consistently produce more polarized audiences. Finally, I would investigate the relationship between a movie's number of ratings, average rating, and rating variability to determine whether highly popular movies tend to receive more consistent or more divided ratings.
