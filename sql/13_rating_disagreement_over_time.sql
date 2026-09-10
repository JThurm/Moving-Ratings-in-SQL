-- measure rating disagreement by release year using standard deviation

SELECT
    m.release_year,
    COUNT(r.rating) AS rating_count,
    ROUND(AVG(r.rating) , 2) AS average_rating,
    ROUND(STDDEV(r.rating), 2) AS rating_stddev
FROM ratings r
JOIN movies m ON r.movie_id = m.movie_id
WHERE m.release_year IS NOT NULL
GROUP BY m.release_year
ORDER BY m.release_year;