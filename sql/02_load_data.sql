-- Run these via psql (not SQLTools) due to file permission issues with COPY.
-- \copy runs client-side, avoiding the Postgres service's restricted file access.

SET client_encoding = 'UTF8';

\copy movies FROM 'C:\Users\judah\OneDrive\Desktop\College Stuff\projects\Moving-Ratings-in-SQL\data\ml-latest-small\movies.csv' DELIMITER ',' CSV HEADER;

\copy ratings FROM 'C:\Users\judah\OneDrive\Desktop\College Stuff\projects\Moving-Ratings-in-SQL\data\ml-latest-small\ratings.csv' DELIMITER ',' CSV HEADER;