CREATE DATABASE IF NOT EXISTS Comp267;
USE Comp267;

CREATE TABLE department(
department_id int primary key auto_increment,
name varchar(100) unique not null,
description text
);

CREATE TABLE district(
district_id int primary key auto_increment,
name varchar(100) unique not null,
description text
);

CREATE TABLE topic(
topic_id int primary key auto_increment,
name varchar(100) unique not null,
description text
);


CREATE TABLE gov_website (
    website_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) UNIQUE NOT NULL,
    url VARCHAR(255) NOT NULL,
    department_id INT,
    district_id INT,         
    topic_id INT,            
    FOREIGN KEY (department_id) REFERENCES department(department_id),
    FOREIGN KEY (district_id) REFERENCES district(district_id),
    FOREIGN KEY (topic_id) REFERENCES topic(topic_id)
);





CREATE TABLE user(
id INT PRIMARY KEY auto_increment,
name text

);

SHOW TABLES;
