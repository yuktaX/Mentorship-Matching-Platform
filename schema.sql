DROP DATABASE IF EXISTS mentify;
create database mentify;
use mentify;

CREATE TABLE mentee (
    mentee_id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    mentee_name VARCHAR(100),
    contact_no VARCHAR(10),
    email_id VARCHAR(100),
    pass_word VARCHAR(15) NOT NULL UNIQUE,
    username VARCHAR(100) UNIQUE not NULL,
    interests VARCHAR(500),
    education VARCHAR(200)

);

CREATE TABLE mentor (
    mentor_id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    mentor_name VARCHAR(100),
    contact_no VARCHAR(10),
    email_id VARCHAR(100),
    qualification VARCHAR(100),
    work_exp VARCHAR(255),
    pass_word VARCHAR(15) NOT NULL UNIQUE,
    username VARCHAR(100) UNIQUE NOT NULL,
    file_name VARCHAR(255)
);


CREATE TABLE category (
    category_id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    category_name VARCHAR(100)
    
);

CREATE TABLE mentee_category (
    category_id INT,
    mentee_id INT,
    PRIMARY KEY (category_id, mentee_id),
    FOREIGN KEY (category_id) REFERENCES category(category_id),
    FOREIGN KEY (mentee_id) REFERENCES mentee(mentee_id)
);

CREATE TABLE mentorship_prog (
    program_id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    mentee_id INT,
    mentor_id INT,
    category_id INT,
    payment INT,
    status VARCHAR(10),
    FOREIGN KEY (mentee_id) REFERENCES mentee(mentee_id),
    FOREIGN KEY (mentor_id) REFERENCES mentor(mentor_id),
    FOREIGN KEY (category_id) REFERENCES category(category_id)
);

CREATE TABLE course (
    program_id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    mentor_id INT,
    course_name VARCHAR(255), 
    no_of_registrations INT DEFAULT 0,
    tag1 VARCHAR(50) DEFAULT 'none',
    tag2 VARCHAR(50) DEFAULT 'none',
    tag3 VARCHAR(50) DEFAULT 'none',
    tag4 VARCHAR(50) DEFAULT 'none',
    tag5 VARCHAR(50) DEFAULT 'none',
    FOREIGN KEY (mentor_id) REFERENCES mentor(mentor_id)
);

INSERT INTO mentee(mentee_name,email_id,username,pass_word) VALUES ('Mimi','arunkumarvaishnovi@gmail.com','mimi','abcd');
INSERT INTO mentor(mentor_name,email_id,username,pass_word,qualification,work_exp) VALUES ('Sneha','vaishnoviarun7060@gmail.com','sneha','1234','BTech',4);
