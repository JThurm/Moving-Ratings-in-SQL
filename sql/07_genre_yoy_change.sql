WITH genre_year AS (
    SELECT
        m.release_year,
        mg.genre,
        ROUND(AVG(r.rating), 2) AS average_rating,
        COUNT(r.rating) AS rating_count
    FROM ratings r
    JOIN movies m ON r.movie_id = m.movie_id
    JOIN movie_genres mg ON m.movie_id = mg.movie_id
    WHERE m.release_year IS NOT NULL
    GROUP BY m.release_year, mg.genre
)
SELECT
    genre,
    release_year,
    average_rating,
    average_rating - LAG(average_rating) OVER (PARTITION BY genre ORDER BY release_year) AS yoy_change
FROM genre_year
ORDER BY genre, release_year;