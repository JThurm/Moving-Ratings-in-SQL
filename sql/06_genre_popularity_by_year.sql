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
ORDER BY m.release_year, mg.genre;
