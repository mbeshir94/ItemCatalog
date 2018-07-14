/*
File name: C:\Users\Mahmoud Beshir\Desktop\BookCatalog1.sql
Creation date: 07/14/2018
Created by SQLite to PostgreSQL 1.5 [Demo]
--------------------------------------------------
More conversion tools at http://www.convert-in.com
*/
DO $$
BEGIN
IF NOT EXISTS (SELECT schema_name FROM information_schema.schemata WHERE schema_name = '')
THEN
CREATE SCHEMA "";
END IF;
END$$;
/*
Table structure for table 'books'
*/

DROP TABLE IF EXISTS "books" CASCADE;
CREATE TABLE "books" (
	"id" INTEGER NOT NULL,
	"bookName" VARCHAR(150)  NOT NULL,
	"authorName" VARCHAR(150)  NOT NULL,
	"coverUrl" VARCHAR(500)  NOT NULL,
	"description" TEXT NOT NULL,
	"category" VARCHAR(150)  NOT NULL,
	"user_id" INTEGER
) WITH OIDS;
DROP INDEX IF EXISTS "PK_books";
ALTER TABLE "books" ADD CONSTRAINT "PK_books" PRIMARY KEY("id");

/*
Dumping data for table 'books'
*/

INSERT INTO "books"("id", "bookName", "authorName", "coverUrl", "description", "category", "user_id") VALUES (1, 'Hello!', 'Janine Amos', 'bla bla', '...', 'Romance', 1);
INSERT INTO "books"("id", "bookName", "authorName", "coverUrl", "description", "category", "user_id") VALUES (2, 'Romantic Poetry, Volume 7', 'Angela Esterhammer', 'bla bla', '...', 'Fantasy', 1);
INSERT INTO "books"("id", "bookName", "authorName", "coverUrl", "description", "category", "user_id") VALUES (3, 'So Not The Drama', 'Paula Chase', 'bla bla', '...', 'Fiction', 1);
INSERT INTO "books"("id", "bookName", "authorName", "coverUrl", "description", "category", "user_id") VALUES (4, 'This Blue Novel', 'Valerie Mejer Caso', 'bla bla', '...', 'Other', 1);

/*
Table structure for table 'categories'
*/

DROP TABLE IF EXISTS "categories" CASCADE;
CREATE TABLE "categories" (
	"id" INTEGER NOT NULL,
	"name" VARCHAR(150)  NOT NULL
) WITH OIDS;
DROP INDEX IF EXISTS "PK_categories";
ALTER TABLE "categories" ADD CONSTRAINT "PK_categories" PRIMARY KEY("id");

/*
Dumping data for table 'categories'
*/

INSERT INTO "categories"("id", "name") VALUES (1, 'Fantasy');
INSERT INTO "categories"("id", "name") VALUES (2, 'Romance');
INSERT INTO "categories"("id", "name") VALUES (3, 'Mystery');
INSERT INTO "categories"("id", "name") VALUES (4, 'Fiction');
INSERT INTO "categories"("id", "name") VALUES (5, 'Horror');
INSERT INTO "categories"("id", "name") VALUES (6, 'Other');

/*
Table structure for table 'user'
*/

DROP TABLE IF EXISTS "user" CASCADE;
CREATE TABLE "user" (
	"id" INTEGER NOT NULL,
	"name" VARCHAR(150)  NOT NULL,
	"email" VARCHAR(150)  NOT NULL,
	"image" VARCHAR(150) ,
	"provider" VARCHAR(20) 
) WITH OIDS;
DROP INDEX IF EXISTS "PK_user";
ALTER TABLE "user" ADD CONSTRAINT "PK_user" PRIMARY KEY("id");

/*
Dumping data for table 'user'
*/

INSERT INTO "user"("id", "name", "email", "image", "provider") VALUES (1, 'admin', 'mahmoud.beshir94@gmail.com', NULL, NULL);
