CREATE TABLE IF NOT EXISTS mainmenu
(
    id    integer PRIMARY KEY AUTOINCREMENT,
    title text NOT NULL,
    url   text NOT NULL
);

CREATE TABLE IF NOT EXISTS posts
(
    id integer PRIMARY KEY AUTOINCREMENT ,
    title text NOT NULL,
    article text NOT NULL,
    created_time integer NOT NULL,
    url text NOT NULL
);

CREATE TABLE IF NOT EXISTS users
(
    id integer PRIMARY KEY AUTOINCREMENT,
    name text NOT NULL,
    email text NOT NULL,
    pwd text NOT NULL,
    avatar BLOB DEFAULT NULL,
    create_time integer NOT NULL
);