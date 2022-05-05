CREATE DATABASE IMDb;

CREATE TABLE IF NOT EXISTS titles (
  title_id 			  VARCHAR(255) NOT NULL PRIMARY KEY,
  title_type 			VARCHAR(50),
  primary_title 	TEXT, -- some are really long
  original_title 	TEXT, -- some are really long
  is_adult 			  BOOLEAN,
  start_year			INTEGER, -- add better domain here (>1800)
  end_year 			  INTEGER, -- add better domain here (>0)
  runtime_minutes	INTEGER -- add better domain here (>0)
);

CREATE TABLE IF NOT EXISTS title_ratings (
  title_id 			  VARCHAR(255) NOT NULL REFERENCES titles(title_id),
  average_rating	FLOAT,
  num_votes			  INTEGER,
  PRIMARY KEY (title_id)
);

CREATE TABLE IF NOT EXISTS aliases (
  title_id          VARCHAR(255) NOT NULL,
  ordering          INTEGER NOT NULL,
  title             TEXT,
  region				    CHAR(4),
  language          CHAR(4),
  is_original_title	INTEGER,
  PRIMARY KEY (title_id,ordering)
);

CREATE TABLE IF NOT EXISTS alias_types (
  title_id      VARCHAR(255) NOT NULL,
  ordering			INTEGER NOT NULL,
  type				  VARCHAR(255) NOT NULL,
  PRIMARY KEY (title_id,ordering)
);

CREATE TABLE IF NOT EXISTS aLias_attributes (
  title_id			VARCHAR(255) NOT NULL,
  ordering			INTEGER NOT NULL,
  attribute			VARCHAR(255) NOT NULL,
  PRIMARY KEY (title_id,ordering)
);

CREATE TABLE IF NOT EXISTS episode_belongs_to (
  episode_title_id          VARCHAR(255) NOT NULL REFERENCES titles (title_id),
  parent_tv_show_title_id   VARCHAR(255) NOT NULL,
  season_number             INTEGER,
  episode_number            INTEGER,
  PRIMARY KEY (episode_title_id)
);

CREATE TABLE IF NOT EXISTS title_genres (
  title_id    VARCHAR(255) NOT NULL REFERENCES titles(title_id),
  genre				VARCHAR(255) NOT NULL,
  PRIMARY KEY (title_id,genre)
);

-- Names and name is a reserved word in MySQL, so we add an underscore

CREATE TABLE IF NOT EXISTS names (
  name_id       VARCHAR(255) NOT NULL PRIMARY KEY,
  name_         VARCHAR(255) NOT NULL,
  birth_year    SMALLINT, -- add a better domain here
  death_year    SMALLINT -- add a better domain here
);

CREATE TABLE IF NOT EXISTS name_worked_as (
  name_id       VARCHAR(255) NOT NULL REFERENCES names (name_id),
  profession    VARCHAR(255) NOT NULL,
  PRIMARY KEY (name_id,profession)
);

-- NOTE: All 3 must must be used as the primary key
-- role is a reserved word in MySQL, so we add an underscore

CREATE TABLE IF NOT EXISTS had_role (
  title_id      VARCHAR(255) NOT NULL, -- not null bc PK
  name_id       VARCHAR(255) NOT NULL, -- not null bc PK
  role_         TEXT -- not null bc PK
);

CREATE TABLE IF NOT EXISTS known_for (
  name_id       VARCHAR(255) NOT NULL REFERENCES names (name_id),
  title_id      VARCHAR(255) NOT NULL,
  PRIMARY KEY (name_id,title_id)
);

CREATE TABLE IF NOT EXISTS directors (
  title_id      VARCHAR(255) NOT NULL REFERENCES titles (title_id),
  name_id       VARCHAR(255) NOT NULL,
  PRIMARY KEY (title_id,name_id)
);

CREATE TABLE IF NOT EXISTS writers (
  title_id      VARCHAR(255) NOT NULL REFERENCES titles (title_id),
  name_id       VARCHAR(255) NOT NULL,
  PRIMARY KEY (title_id,name_id)
);

CREATE TABLE IF NOT EXISTS principals (
  title_id      VARCHAR(255) NOT NULL,
  ordering      SMALLINT NOT NULL,
  name_id       VARCHAR(255) NOT NULL,
  job_category  VARCHAR(255),
  job           TEXT,
  PRIMARY KEY (title_id,ordering)
);