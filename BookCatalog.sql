DROP TABLE IF EXISTS `books`;
CREATE TABLE `books` (
  `id` integer NOT NULL,
  `bookName` varchar(150) NOT NULL,
  `authorName` varchar(150) NOT NULL,
  `coverUrl` varchar(500) NOT NULL,
  `description` varchar(256) NOT NULL,
  `category` varchar(150) NOT NULL,
  `user_id` integer,
  PRIMARY KEY (`id`),
  FOREIGN KEY (user_id) REFERENCES user (id)
);

INSERT INTO `books` (`id`,`bookName`,`authorName`,`coverUrl`,`description`,`category`,`user_id`) VALUES (1,'Hello!','Janine Amos','bla bla','...','Romance',1);
INSERT INTO `books` (`id`,`bookName`,`authorName`,`coverUrl`,`description`,`category`,`user_id`) VALUES (2,'Romantic Poetry, Volume 7','Angela Esterhammer','bla bla','...','Fantasy',1);
INSERT INTO `books` (`id`,`bookName`,`authorName`,`coverUrl`,`description`,`category`,`user_id`) VALUES (3,'So Not The Drama','Paula Chase','bla bla','...','Fiction',1);
INSERT INTO `books` (`id`,`bookName`,`authorName`,`coverUrl`,`description`,`category`,`user_id`) VALUES (4,'This Blue Novel','Valerie Mejer Caso','bla bla','...','Other',1);
DROP TABLE IF EXISTS `categories`;
CREATE TABLE `categories` (
  `id` integer NOT NULL,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`)
);

INSERT INTO `categories` (`id`,`name`) VALUES (1,'Fantasy');
INSERT INTO `categories` (`id`,`name`) VALUES (2,'Romance');
INSERT INTO `categories` (`id`,`name`) VALUES (3,'Mystery');
INSERT INTO `categories` (`id`,`name`) VALUES (4,'Fiction');
INSERT INTO `categories` (`id`,`name`) VALUES (5,'Horror');
INSERT INTO `categories` (`id`,`name`) VALUES (6,'Other');
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` integer NOT NULL,
  `name` varchar(150) NOT NULL,
  `email` varchar(150) NOT NULL,
  `image` varchar(150),
  `provider` varchar(20),
  PRIMARY KEY (`id`)
);

INSERT INTO `user` (`id`,`name`,`email`,`image`,`provider`) VALUES (1,'admin','mahmoud.beshir94@gmail.com',NULL,NULL);