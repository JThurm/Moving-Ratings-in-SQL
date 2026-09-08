CREATE TABLE movies (
    movie_id  INT PRIMARY KEY,
    title     VARCHAR(255) NOT NULL,
    genres     VARCHAR(255) NOT NULL
);

CREATE TABLE ratings (
    user_id  INT NOT NULL,
    movie_id INT NOT NULL REFERENCES movies(movie_id),
    rating   DECIMAL(2, 1) NOT NULL,
    timestamp BIGINT NOT NULL,
    ALTER TABLE ratings RENAME COLUMN timestamp TO rated_at;
    PRIMARY KEY (user_id, movie_id)
);

