-- Comparing genre trends across major historical eras
-- Rating volume is used as the popularity meausre

WITH era_data AS(
    SELECT
        m.release_year,
        CASE 
            WHEN m.release_year BETWEEN 1900 AND 1929 THEN 'Early Cinema'
            WHEN m.release_year BETWEEN 1930 AND 1945 THEN 'The Great Depression and WWII'
            WHEN m.release_year BETWEEN 1946 AND 1959 THEN 'Postwar Cinema'
            WHEN m.release_year BETWEEN 1960 AND 1979 THEN 'New Hollywood'
            WHEN m.release_year BETWEEN 1980 AND 1999 THEN 'Blockbuster Era'
            WHEN m.release_year BETWEEN 2000 AND 2006 THEN 'Early Digital'
            WHEN m.release_year BETWEEN 2007 AND 2018 THEN 'Streaming Era' 
        END AS historical_era,
        CASE 
            WHEN m.release_year BETWEEN 1900 AND 1929 THEN 1
            WHEN m.release_year BETWEEN 1900 AND 1929 THEN 2
            WHEN m.release_year BETWEEN 1900 AND 1929 THEN 3
            WHEN m.release_year BETWEEN 1900 AND 1929 THEN 4
            WHEN m.release_year BETWEEN 1900 AND 1929 THEN 5
            WHEN m.release_year BETWEEN 1900 AND 1929 THEN 6
            WHEN m.release_year BETWEEN 1900 AND 1929 THEN 7
        END AS era_order,
        mg.genre,
        r.rating
    FROM ratings r
    JOIN movies m ON r.movie_id = m.movie_id
    JOIN movie_genres mg ON m.movie_id = mg.movie_id
    WHERE m.release_year IS NOT NULL
        AND mg.genre <> '(no genres listed)'
)
SELECT
    historical_era,
    genre,
    COUNT(*) AS rating_count,
    ROUND(AVG(rating), 2) AS average_rating,
    era_order
FROM era_data
GROUP BY historical_era, genre, era_order
ORDER BY era_order, rating_count DESC, genre;