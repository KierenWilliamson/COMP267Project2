CREATE DATABASE Comp267 IF NOT EXISTS;
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


CREATE TABLE gov_website(
website_id INT PRIMARY KEY auto_increment,
name varchar(100) unique not null,
url varchar(255) not null,
FOREIGN KEY (department_id) REFERENCES department(department_id),
FOREIGN KEY (district_id) REFERENCES district(district_id),
FOREIGN KEY (topic_id) REFERENCES topic(topic_id)
);


SHOW TABLES;



CREATE TABLE user(
id INT PRIMARY KEY auto_increment,
name text

);