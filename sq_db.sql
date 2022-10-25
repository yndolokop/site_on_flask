

CREATE TABLE IF NOT EXISTS mainmenu (
id integer PRIMARY KEY AUTOINCREMENT,
title text NOT NULL,
url text NOT NULL
);

CREATE TABLE IF NOT EXISTS person (
id integer PRIMARY KEY AUTOINCREMENT,
field text NOT NULL,
region text NOT NULL,
skill text NOT NULL,
count integer NOT NULL,
percent real NOT NULL,
time integer NOT NULL
);

DROP TABLE IF EXISTS result; CREATE TABLE result (
id integer PRIMARY KEY AUTOINCREMENT,
field_name text NOT NULL,
region_name text NOT NULL,
data json NOT NULL,
time integer NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
id integer PRIMARY KEY AUTOINCREMENT,
name text NOT NULL,
email text NOT NULL,
psw text NOT NULL,
avatar BLOB DEFAULT NULL,
time integer NOT NULL
);