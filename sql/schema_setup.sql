CREATE TABLE movies (
    movie_id  INT PRIMARY KEY,
    title     VARCHAR(255) NOT NULL,
    genres     VARCHAR(255) NOT NULL
);

SELECT * FROM movies LIMIT 10;

CREATE TABLE ratings (
    user_id  INT NOT NULL,
    movie_id INT NOT NULL REFERENCES movies(movie_id),
    rating   DECIMAL(2, 1) NOT NULL,
    timestamp BIGINT NOT NULL,
    PRIMARY KEY (user_id, movie_id)
);

SELECT * FROM ratings LIMIT 10;