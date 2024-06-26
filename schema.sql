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



CREATE TABLE course (
    course_id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    mentor_id INT,
    course_name VARCHAR(255) NOT NULL, 
    max_limit INT,
    course_start DATE,
    course_end DATE,
    course_price INT,
    course_status ENUM('unverified', 'verified','rejected') DEFAULT 'unverified',
    admin_comment VARCHAR(500),
    course_desc VARCHAR(500),
    index(course_name),
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
    course_id INT,
    mentee_id INT,
    complaint_date DATE,
    complaint_desc VARCHAR(500),
    complaint_status ENUM('pending', 'resolved') DEFAULT 'pending',
    complaint_action VARCHAR(500),
    FOREIGN KEY (mentee_id) REFERENCES mentee(mentee_id),
    FOREIGN KEY (course_id) REFERENCES course(course_id)


);

CREATE TABLE mentor_complaints(
    complaint_id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    mentee_id INT,
    course_id INT,
    complaint_date DATE,
    complaint_desc VARCHAR(500),
    complaint_status ENUM('pending', 'resolved') DEFAULT 'pending',
    complaint_action VARCHAR(500),
    FOREIGN KEY (mentee_id) REFERENCES mentee(mentee_id),
    FOREIGN KEY (course_id) REFERENCES course(course_id)

);
CREATE TABLE course_mentee(
    course_mentee_id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    mentee_id INT,
    course_id INT,
    FOREIGN KEY (mentee_id) REFERENCES mentee(mentee_id),
    FOREIGN KEY (course_id) REFERENCES course(course_id)

);


CREATE TABLE messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sender VARCHAR(100) NOT NULL,
    content TEXT NOT NULL,
    course_id INT NOT NULL,
    FOREIGN KEY (course_id) REFERENCES course(course_id)
);

CREATE TABLE feedback (
    feedback_id INT AUTO_INCREMENT PRIMARY KEY,
    course_id INT,
    rating INT,
    feedback_comments VARCHAR(255),
    FOREIGN KEY (course_id) REFERENCES course(course_id)
);


INSERT INTO tag(tag_name) VALUES ('Product Management');
INSERT INTO tag(tag_name) VALUES ('Soft Skills');
INSERT INTO tag(tag_name) VALUES ('Network Security');
INSERT INTO mentee(mentee_name,email_id,username,pass_word) VALUES ('Mimi','vaishnoviarun7060@gmail.com','mimi','abcd');
INSERT INTO mentor(mentor_name,email_id,username,pass_word,degree,work_exp,mentor_status) VALUES ('Sneha','sneha@example.com','sneha','1234','BTech',4,"unverified");
insert into course(mentor_id,course_name,course_start,course_end,course_price,course_desc) values(1,'data structures','2024-01-03','2024-03-29','500','A complete beginnner to advanced data structures course');
INSERT INTO messages (sender, content, course_id) VALUES
('Sneha','Hello!', 1),
('Mimi', 'Hi there!',1);
