SELECT
    m.title,
    COUNT(r.rating) AS num_ratings,
    ROUND(AVG(r.rating), 2) AS average_rating,
    ROUND(STDDEV(r.rating), 2) AS rating_stddev
FROM ratings r
JOIN movies m ON r.movie_id = m.movie_id
GROUP BY m.title, m.movie_id
HAVING COUNT(r.rating) >= 100
ORDER BY rating_stddev DESC
LIMIT 20;