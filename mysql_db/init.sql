/* Create tables on container start up */
CREATE TABLE `articles` (
  `article_id` varchar(90) NOT NULL,
  `headline` varchar(450) NOT NULL,
  `published_time` datetime NOT NULL,
  `publisher_timezone` varchar(90) NOT NULL,
  `article_content` longtext,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_by` varchar(45) NOT NULL,
  PRIMARY KEY (`article_id`),
  KEY `timezone_idx` (`publisher_timezone`),
  KEY `publish_time_idx` (`published_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `entities` (
  `entity_id` int(11) NOT NULL AUTO_INCREMENT,
  `article_id` varchar(45) NOT NULL,
  `entity` varchar(45) NOT NULL,
  `entity_value` varchar(90) NOT NULL,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_by` varchar(45) NOT NULL,
  PRIMARY KEY (`entity_id`),
  KEY `entity_entity_value_idx` (`entity`,`entity_value`),
  KEY `entity_article_idx_idx` (`article_id`),
  CONSTRAINT `article_id_fk_2` FOREIGN KEY (`article_id`) REFERENCES `articles` (`article_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `tags` (
  `tag_id` int(11) NOT NULL AUTO_INCREMENT,
  `article_id` varchar(45) NOT NULL,
  `tag` varchar(45) NOT NULL,
  `tagged_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `tagged_by` varchar(45) NOT NULL,
  PRIMARY KEY (`tag_id`),
  UNIQUE KEY `article_tag_unique` (`article_id`,`tag`),
  KEY `article_id_idx` (`article_id`),
  KEY `tag_idx` (`tag`),
  CONSTRAINT `article_id_fk_1` FOREIGN KEY (`article_id`) REFERENCES `articles` (`article_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


/* Populate tables with sample data */
INSERT INTO `articles`
VALUES ('abc123', 'click baity headline', '2021-01-01 12:05:00', 'America/Toronto', 'sensational stuff',  CURRENT_TIMESTAMP, 'user1');

INSERT INTO `articles`
VALUES ('abc456', 'cool headline', '2022-01-01 11:59:00', 'America/Montreal', 'cool stuff', CURRENT_TIMESTAMP, 'user2');

INSERT INTO `entities`
VALUES (1, 'abc123', 'city', 'toronto', CURRENT_TIMESTAMP, 'user1');

INSERT INTO `entities`
VALUES (2, 'abc123', 'city', 'montreal', CURRENT_TIMESTAMP, 'user1');

INSERT INTO `entities`
VALUES (3, 'abc123', 'organization', 'pfizer', CURRENT_TIMESTAMP, 'user1');

INSERT INTO `entities`
VALUES (4, 'abc123', 'organization', 'ramq', CURRENT_TIMESTAMP, 'user1');

INSERT INTO `entities`
VALUES (5, 'abc123', 'topic', 'health', CURRENT_TIMESTAMP, 'user1');

INSERT INTO `entities`
VALUES (6, 'abc123', 'topic', 'vaccine', CURRENT_TIMESTAMP, 'user1');

INSERT INTO `entities`
VALUES (7, 'abc123', 'topic', 'covid-19', CURRENT_TIMESTAMP, 'user1');

INSERT INTO `entities`
VALUES (8, 'abc456', 'city', 'montreal', CURRENT_TIMESTAMP, 'user1');

INSERT INTO `entities`
VALUES (9, 'abc456', 'organization', 'just for laughs', CURRENT_TIMESTAMP, 'user1');

INSERT INTO `entities`
VALUES (10, 'abc456', 'topic', 'comedy', CURRENT_TIMESTAMP, 'user1');