-- Compare selected historical / industry events with genre and rating trends.
-- These events are contextual markers, not causal variables

WITH events AS (
    SELECT *
    FROM (VALUES
        (1929, 1939, 'Great Depression', 'Economic'),
        (1939, 1945, 'World War II', 'Historical'),
        (1977, 1977, 'Star Wars release', 'Franchise'),
        (1993, 1993, 'Jurassic Park release', 'Franchise'),
        (2001, 2003, 'The Lord of the Rings trilogy', 'Franchise'),
        (2007, 2007, 'Netflix begins streaming', 'Streaming'),
        (2008, 2008, 'Iron Man / MCU launch', 'Franchise'),
        (2010, 2010, 'Instagram launch', 'Digital'),
        (2015, 2015, 'Major streaming expansion', 'Streaming')
    ) AS v(start_year, end_year, event_name, event_type)
),
year_stats AS (
    SELECT
        m.release_year,
        mg.genre,
        COUNT(r.rating) AS rating_count,
        ROUND(AVG(r.rating), 2) AS average_rating,
        ROUND(STDDEV(r.rating), 2) AS rating_stddev
    FROM ratings r
    JOIN movies m ON r.movie_id = m.movie_id
    JOIN movie_genres mg ON m.movie_id = mg.movie_id
    WHERE m.release_year IS NOT NULL
      AND mg.genre <> '(no genres listed)'
    GROUP BY m.release_year, mg.genre
)
SELECT
    ys.release_year,
    e.event_name,
    e.event_type,
    ys.genre,
    ys.rating_count,
    ys.average_rating,
    ys.rating_stddev
FROM year_stats ys
LEFT JOIN events e
    ON ys.release_year BETWEEN e.start_year AND e.end_year
WHERE e.event_name IS NOT NULL
ORDER BY ys.release_year, e.event_name, ys.rating_count DESC, ys.genre;