CREATE TABLE movie_genres (
    movie_id INT NOT NULL REFERENCES movies(movie_id),
    genre    VARCHAR(255) NOT NULL,
    PRIMARY KEY (movie_id, genre)
);

INSERT INTO movie_genres (movie_id, genre)
SELECT
    movie_id,
    unnest(string_to_array(genres, '|')) 
FROM movies;