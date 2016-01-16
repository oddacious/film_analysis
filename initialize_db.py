#!/usr/bin/python

import sqlite3

import db_wrapper

create_lists = """
CREATE TABLE IF NOT EXISTS {0}
(
    id INTEGER PRIMARY KEY,
    list_link TEXT UNIQUE,
    list_name TEXT,
    size INT,
    favs INT,
    dislikes INT,
    description TEXT,
    user TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
);
"""

create_list_tags = """
CREATE TABLE IF NOT EXISTS {0}
(
    id INTEGER PRIMARY KEY,
    list_link TEXT,
    tag TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
);
"""

create_list_progress = """
CREATE TABLE IF NOT EXISTS {0}
(
    id INTEGER PRIMARY KEY,
    user TEXT,
    list_link TEXT,
    seen INT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
);
"""

create_films = """
CREATE TABLE IF NOT EXISTS {0}
(
    id INTEGER PRIMARY KEY,
    film_link TEXT UNIQUE,
    film_name TEXT,
    year INT,
    num_lists INT,
    user TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
);
"""

create_film_tags = """
CREATE TABLE IF NOT EXISTS {0}
(
    id INTEGER PRIMARY KEY,
    film_link TEXT,
    tag TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
);
"""

create_film_progress = """
CREATE TABLE IF NOT EXISTS {0}
(
    id INTEGER PRIMARY KEY,
    user TEXT
    film_link TEXT,
    seen INT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
);
"""

create_list_items = """
CREATE TABLE IF NOT EXISTS {0}
(
    id INTEGER PRIMARY KEY,
    list_link TEXT,
    film_link TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
);
"""

def initialize_db(dbname='icheckmovies.db'):
    db = db_wrapper.db_wrapper(dbname)
    db.init_table("lists", create_lists)
    db.init_table("list_tags", create_list_tags)
    db.init_table("list_progress", create_list_progress)
    db.init_table("films", create_films)
    db.init_table("film_tags", create_film_tags)
    db.init_table("film_progress", create_film_progress)
    db.init_table("list_items", create_list_items)

if __name__ == "__main__":
    initialize_db()
