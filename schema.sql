DROP DATABASE IF EXISTS mentify;
create database mentify;
use mentify;

CREATE TABLE mentee (
  mentee_id  INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  mentee_name VARCHAR(255) NOT NULL,
  contact_no INT,
  email_id VARCHAR(255) NOT NULL,
  username VARCHAR(100) NOT NULL,
  pass_word VARCHAR(100) NOT NULL
);

CREATE TABLE mentor (
  mentor_id  INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  mentor_name VARCHAR(255) NOT NULL,
  contact_no INT,
  email_id VARCHAR(255) NOT NULL,
  username VARCHAR(100) NOT NULL,
  pass_word VARCHAR(100) NOT NULL,
  qualification VARCHAR(100) NOT NULL,
  work_experience INT NOT NULL
);

INSERT INTO mentee(mentee_name,email_id,username,pass_word) VALUES ('Mimi','mimi@gmail.com','mimi','abcd');
INSERT INTO mentor(mentor_name,email_id,username,pass_word,qualification,work_experience) VALUES ('Sneha','sneha@gmail.com','sneha','1234','BTech',4);