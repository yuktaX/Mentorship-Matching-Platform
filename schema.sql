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
    degree VARCHAR(100),
    institute VARCHAR(100),
    major VARCHAR(100),
    work_exp VARCHAR(255),
    pass_word VARCHAR(15) NOT NULL UNIQUE,
    username VARCHAR(100) UNIQUE NOT NULL,
    file_name VARCHAR(255),
    mentor_status VARCHAR(20) NOT NULL,
    interests VARCHAR(500)
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
    course_id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    mentor_id INT,
    course_name VARCHAR(255), 
    no_of_registrations INT DEFAULT 0,
    course_start DATE,
    course_end DATE,
    course_price INT,
    course_status VARCHAR(20),
    course_desc VARCHAR(500),
    
    FOREIGN KEY (mentor_id) REFERENCES mentor(mentor_id)
);

CREATE TABLE tag(
    tag_id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    tag_name VARCHAR(100)
);

CREATE TABLE course_tag_relation(
    course_tag_id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    course_id INT,
    tag_id INT,
    FOREIGN KEY (tag_id) REFERENCES tag(tag_id),
    FOREIGN KEY (course_id) REFERENCES course(course_id)

);

CREATE TABLE mentee_tag(
    mentee_tag_id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    mentee_id INT,
    tag_id INT,
    FOREIGN KEY (tag_id) REFERENCES tag(tag_id),
    FOREIGN KEY (mentee_id) REFERENCES mentee(mentee_id)

);

CREATE TABLE mentee_complaints(
    complaint_id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    mentee_id INT,
    complaint_date DATE,
    complaint_desc VARCHAR(500),
    complaint_status VARCHAR(20),
    complaint_action VARCHAR(500),
    FOREIGN KEY (mentee_id) REFERENCES mentee(mentee_id)

);

CREATE TABLE mentor_complaints(
    complaint_id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    mentor_id INT,
    complaint_date DATE,
    complaint_desc VARCHAR(500),
    complaint_status VARCHAR(20),
    complaint_action VARCHAR(500),
    FOREIGN KEY (mentor_id) REFERENCES mentor(mentor_id)

);




INSERT INTO mentee(mentee_name,email_id,username,pass_word) VALUES ('Mimi','mimi@example.com','mimi','abcd');
INSERT INTO mentor(mentor_name,email_id,username,pass_word,degree,work_exp,mentor_status) VALUES ('Sneha','sneha@example.com','sneha','1234','BTech',4,"unverified");
