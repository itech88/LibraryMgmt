DROP DATABASE IF EXISTS `library`;
CREATE DATABASE library;
USE `library`;

SET NAMES utf8 ;
SET character_set_client = utf8mb4 ;

CREATE TABLE Books (
    id INT AUTO_INCREMENT,
    title VARCHAR(255),
    author VARCHAR(255),
    publish_date DATE,
    available BOOLEAN,
    PRIMARY KEY (id)
);




ALTER TABLE Books
ADD copies INT;

ALTER TABLE Books
ADD checked_out INT;


ALTER TABLE Books
MODIFY COLUMN available AS (copies > 0);

ALTER TABLE Books
ADD is_checked_out AS (checked_out > 0);
