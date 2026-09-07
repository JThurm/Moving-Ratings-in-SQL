ALTER TABLE movies ADD COLUMN release_year INT;
UPDATE movies
SET release_year = CAST(SUBSTRING(title FROM '\((\d{4})\)$') AS INT)
WHERE title ~ '\(\d{4}\)$';