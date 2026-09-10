-- Comparing rating disagreement across genres
-- Ratings for multi-genre3 movies contribute to each assigned genre

WITH genre_stats AS (
    SELECT
        mg.genre,
        COUNT(r.rating) AS rating_count,
        ROUND(AVG(r.rating), 2) AS average_rating,
        ROUND(STDDEV(r.rating), 2) AS rating_stddev
    FROM ratings r
    JOIN movies m ON r.movie_id = m.movie_id
    JOIN movie_genres mg ON m.movie_id = mg.movie_id
    WHERE mg.genre <> '(no genres listed)'
    GROUP BY mg.genre
    HAVING COUNT(r.rating) >= 100
)
SELECT
    genre,
    rating_count,
    average_rating,
    rating_stddev,
    RANK() OVER (ORDER BY rating_stddev DESC) AS polarization_rank
FROM genre_stats
ORDER BY polarization_rank, genre;
