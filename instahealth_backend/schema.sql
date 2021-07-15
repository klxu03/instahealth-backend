DROP TABLE IF EXISTS users;

CREATE TABLE users (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	email TEXT UNIQUE NOT NULL,
	password TEXT NOT NULL,
	role TEXT NOT NULL
);

DROP TABLE IF EXISTS questions;

CREATE TABLE questions (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	question TEXT NOT NULL,
	content TEXT NOT NULL,
	authorName TEXT NOT NULL,
	tags TEXT NOT NULL,
	datePosted INTEGER DEFAULT (CAST(strftime('%s','now') as int))
);

DROP TABLE IF EXISTS answers;

CREATE TABLE answers (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	questionId INTEGER NOT NULL,
	content TEXT NOT NULL,
	role TEXT NOT NULL,
	authorName TEXT NOT NULL,
	datePosted INTEGER DEFAULT (CAST(strftime('%s','now') as int)),
	FOREIGN KEY (questionId) REFERENCES questions (id)
);
