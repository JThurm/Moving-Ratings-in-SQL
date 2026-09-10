-- Investigating the relationship between rating volume
-- average rating, and rating varanbility at movie level

WITH movie_stats AS (
    SELECT
        m.movie_id,
        m.title,
        m.release_year,
        COUNT(r.rating) AS rating_count,
        ROUND(AVG(r.rating), 2) AS average_rating,
        ROUND(STDDEV(r.rating), 2) AS rating_stddev
    FROM ratings r
    JOIN movies m ON r.movie_id = m.movie_id
    WHERE m.release_year IS NOT NULL
    GROUP BY m.movie_id, m.title, m.release_year
    HAVING COUNT(r.rating) >= 20
),
correlation AS (
    SELECT
        CORR(rating_count::double precision, rating_stddev::double precision)
            AS volume_vs_variability,
        CORR(rating_count::double precision, average_rating::double precision)
            AS volume_vs_average,
        CORR(average_rating::double precision, rating_stddev::double precision)
            AS average_vs_variability
    FROM movie_stats
)
SELECT
    ms.*,
    ROUND(c.volume_vs_variability::numeric, 3) AS volume_vs_variability,
    ROUND(c.volume_vs_average::numeric, 3) AS volume_vs_average,
    ROUND(c.average_vs_variability::numeric, 3) AS average_vs_variability
FROM movie_stats ms
CROSS JOIN correlation c
ORDER BY ms.rating_count DESC, ms.title;
