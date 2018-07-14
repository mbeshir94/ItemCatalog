--
-- File generated with SQLiteStudio v3.1.1 on Sat Jul 14 14:23:32 2018
--
-- Text encoding used: UTF-8
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: books
DROP TABLE IF EXISTS books;
CREATE TABLE books (
	id INTEGER NOT NULL, 
	"bookName" VARCHAR(150) NOT NULL, 
	"authorName" VARCHAR(150) NOT NULL, 
	"coverUrl" VARCHAR(500) NOT NULL, 
	description VARCHAR NOT NULL, 
	category VARCHAR(150) NOT NULL, 
	user_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES user (id)
);
INSERT INTO books (id, bookName, authorName, coverUrl, description, category, user_id) VALUES (1, 'Hello!', 'Janine Amos', 'bla bla', '...', 'Romance', 1);
INSERT INTO books (id, bookName, authorName, coverUrl, description, category, user_id) VALUES (2, 'Romantic Poetry, Volume 7', 'Angela Esterhammer', 'bla bla', '...', 'Fantasy', 1);
INSERT INTO books (id, bookName, authorName, coverUrl, description, category, user_id) VALUES (3, 'So Not The Drama', 'Paula Chase', 'bla bla', '...', 'Fiction', 1);
INSERT INTO books (id, bookName, authorName, coverUrl, description, category, user_id) VALUES (4, 'This Blue Novel', 'Valerie Mejer Caso', 'bla bla', '...', 'Other', 1);

-- Table: categories
DROP TABLE IF EXISTS categories;
CREATE TABLE categories (
	id INTEGER NOT NULL, 
	name VARCHAR(150) NOT NULL, 
	PRIMARY KEY (id)
);
INSERT INTO categories (id, name) VALUES (1, 'Fantasy');
INSERT INTO categories (id, name) VALUES (2, 'Romance');
INSERT INTO categories (id, name) VALUES (3, 'Mystery');
INSERT INTO categories (id, name) VALUES (4, 'Fiction');
INSERT INTO categories (id, name) VALUES (5, 'Horror');
INSERT INTO categories (id, name) VALUES (6, 'Other');

-- Table: user
DROP TABLE IF EXISTS user;
CREATE TABLE user (
	id INTEGER NOT NULL, 
	name VARCHAR(150) NOT NULL, 
	email VARCHAR(150) NOT NULL, 
	image VARCHAR(150), 
	provider VARCHAR(20), 
	PRIMARY KEY (id)
);
INSERT INTO user (id, name, email, image, provider) VALUES (1, 'admin', 'mahmoud.beshir94@gmail.com', NULL, NULL);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
