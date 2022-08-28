

CREATE TABLE IF NOT EXISTS mainmenu (
id integer PRIMARY KEY AUTOINCREMENT,
title text NOT NULL,
url text NOT NULL
);

CREATE TABLE IF NOT EXISTS person (
id integer PRIMARY KEY AUTOINCREMENT,
name text NOT NULL,
count integer NOT NULL,
percent real NOT NULL,
time integer NOT NULL
);

CREATE TABLE IF NOT EXISTS skills (
id integer PRIMARY KEY AUTOINCREMENT,
search_by_name text NOT NULL,
requirements text NOT NULL,
vac_name_url text NOT NULL,
time integer NOT NULL
);