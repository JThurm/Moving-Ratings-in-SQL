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
      AND mg.genre != '(no genres listed)'
      GROUP BY m.release_year, mg.genre
    HAVING COUNT(r.rating) >= 50
),
ranked AS (
    SELECT
        *,
        RANK() OVER (PARTITION BY release_year ORDER BY average_rating DESC) AS rnk
    FROM genre_year
)
SELECT release_year, genre, average_rating, rating_count
FROM ranked
WHERE rnk = 1
ORDER BY release_year;