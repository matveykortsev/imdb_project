-- Load Titles.tsv into Titles table
COPY titles
FROM '/data/titles.tsv'
WITH (
FORMAT CSV,
DELIMITER E'\t',
NULL '\N',
FORCE_NULL (end_year),
HEADER);

-- Load Names_.tsv into Names_ table
COPY names
FROM '/data/names.tsv'
WITH (
FORMAT CSV,
DELIMITER E'\t',
NULL '\N',
FORCE_NULL (birth_year,death_year),
HEADER);

-- Load Aliases.tsv into Aliases table
COPY aliases
FROM '/data/aliases.tsv'
WITH(
FORMAT CSV,
DELIMITER E'\t',
NULL '\N',
FORCE_NULL (is_original_title),
HEADER);

-- Load Alias_attributes.tsv into Alias_attributes table
COPY alias_attributes
FROM '/data/alias_attributes.tsv'
DELIMITER E'\t'
CSV HEADER;

-- Load Alias_types.tsv into Alias_types table
COPY alias_types
FROM '/data/alias_types.tsv'
DELIMITER E'\t'
CSV HEADER;


-- Load Writers.tsv into Writers table
COPY writers
FROM '/data/writers.tsv'
DELIMITER E'\t'
CSV HEADER;

-- Load Episode_belongs_to.tsv into Episode_belongs_to table
COPY episode_belongs_to
FROM '/data/episode_belongs_to.tsv'
WITH (
FORMAT CSV,
DELIMITER E'\t',
NULL '\N',
FORCE_NULL (season_number, episode_number),
HEADER);

-- Load Name_worked_as.tsv into Name_worked_as table
COPY name_worked_as
FROM '/data/name_worked_as.tsv'
DELIMITER E'\t'
CSV HEADER;

-- Load Known_for.tsv into Known_for table
COPY known_for
FROM '/data/known_for.tsv'
DELIMITER E'\t'
CSV HEADER;

-- Load Principals.tsv into Principals table
COPY principals
FROM '/data/principals.tsv'
DELIMITER E'\t'
CSV HEADER;

-- Load Had_role.tsv into Had_role table
COPY had_role
FROM '/data/had_role.tsv'
DELIMITER E'\t'
CSV HEADER;


-- Load Title_genres.tsv into Title_genres table
COPY title_genres
FROM '/data/title_genres.tsv'
DELIMITER E'\t'
CSV HEADER;

-- Load Title_ratings.tsv into Title_ratings table
COPY title_ratings
FROM '/data/title_ratings.tsv'
DELIMITER E'\t'
CSV HEADER;