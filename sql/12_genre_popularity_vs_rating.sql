-- Comparting genre popularity (rating volume) with averge rating
-- A minimum of 100 ratings reduces the effect of very small

WITH genre_stats AS (
    SELECT
        mg.genre,
        COUNT(r.rating) AS rating_count,
        ROUND(AVG(r.rating), 2) AS average_rating
    FROM ratings r 
    JOIN movies m ON r.movie_id = m.movie_id
    JOIN movie_genres mg ON m.movie_id = mg.movie_id
    WHERE m.release_year IS NOT NULL
        AND mg.genre <> '(no genres listed)'
    GROUP BY mg.genre
    HAVING COUNT(r.rating) >= 100
)
SELECT
    genre,
    rating_count,
    average_rating,
    RANK() OVER (ORDER BY rating_count DESC) AS popularity_rank,
    RANK() OVER (ORDER BY average_rating DESC) AS rating_rank
FROM genre_stats
ORDER BY popularity_rank, genre;