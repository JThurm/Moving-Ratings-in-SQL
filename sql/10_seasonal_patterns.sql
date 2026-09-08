SELECT
    EXTRACT(YEAR FROM to_timestamp(r.rated_at)) AS rating_year,
    EXTRACT(MONTH FROM to_timestamp(r.rated_at)) AS rating_month,
    ROUND(AVG(rating), 2) AS average_rating,
    COUNT(*) AS num_ratings
FROM ratings r
GROUP BY rating_year, rating_month
ORDER BY rating_year, rating_month;