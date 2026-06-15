CREATE DATABASE college_db;

USE college_db;

CREATE TABLE departments (
    department_id INT AUTO_INCREMENT PRIMARY KEY,
    dept_name VARCHAR(100) NOT NULL,
    hod_name VARCHAR(100),
    budget DECIMAL(12,2)
);
insert into departments (department_id, dept_name, hod_name, budget) value
(001, 'CSE', 'Janani', 80000),
(002, 'ECE', 'Arul', 50000),
(003, 'AIDS', 'Praveen', 85000),
(004, 'VLSI', 'Raja', 100000),
(005, 'MECH', 'Gokul', 540000);
CREATE TABLE students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    date_of_birth DATE,
    department_id INT,
    enrollment_year INT,
    FOREIGN KEY (department_id)
    REFERENCES departments(department_id)
);
insert into students (student_id, first_name, last_name, email, date_of_birth, enrollment_year) value
(1, 'Gopal', 'P', 'abc@gmail.com', '2006-02-11', 2027),
(2, 'Aswin', 'S', 'def@gmail.com', '2005-05-20', 2027),
(3, 'Aananth', 'K', 'hij@gmail.com', '2006-01-10', 2027),
(4, 'Deepak', 'R', 'klm@gmail.com', '2006-07-25', 2027),
(5, 'Vinoj', 'M', 'nop@gmail.com', '2006-11-22', 2027);
UPDATE students
SET department_id = 1
WHERE student_id = 1;

UPDATE students
SET department_id = 2
WHERE student_id = 2;

UPDATE students
SET department_id = 1
WHERE student_id = 3;

UPDATE students
SET department_id = 3
WHERE student_id = 4;

UPDATE students
SET department_id = 2
WHERE student_id = 5;
CREATE TABLE courses (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    course_name VARCHAR(150) NOT NULL,
    course_code VARCHAR(20) UNIQUE,
    credits INT,
    department_id INT,
    FOREIGN KEY (department_id)
    REFERENCES departments(department_id)
);
insert into courses (course_id, course_name, course_code, credits, department_id) values
(001, 'DBMS', 'DB2358', 5, 001),
(002, 'NLP', 'CS2561', 4, 001),
(003, 'OS', 'CS4563', 3, 001),
(004, 'MLT', 'CS8523', 5, 005),
(005, 'DLT', 'CS3245', 4, 003);
CREATE TABLE professors (
    professor_id INT AUTO_INCREMENT PRIMARY KEY,
    prof_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    department_id INT,
    salary DECIMAL(10,2),
    FOREIGN KEY (department_id)
    REFERENCES departments(department_id)
);
insert into professors (professor_id, prof_name, email, department_id, salary) value
(01, 'Magesh', 'qrs@gmail.com', 1, 80000),
(02, 'Aravind', 'tuv@gmail.com', 2, 50000),
(03, 'Sivanandham', 'wxy@gmail.com', 3, 40000),
(04, 'Harish', 'zab@gmail.com', 4, 45890),
(05, 'Raj', 'pol@gmail.com', 3, 36547);
CREATE TABLE enrollments (
    enrollment_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    enrollment_date DATE,
    grade CHAR(2),
    FOREIGN KEY (student_id)
    REFERENCES students(student_id),
    FOREIGN KEY (course_id)
    REFERENCES courses(course_id)
);
insert into enrollments (enrollment_id, student_id, course_id, enrollment_date, grade) values
(01, 1, 001, '2023-05-11', 'A'),
(02, 1, 001, '2023-05-11', 'A'),
(03, 2, 002, '2023-05-11', 'B'),
(04, 3, 003, '2023-05-11', 'A'),
(05, 4, 004, '2023-05-11', 'C');
ALTER TABLE students
ADD COLUMN phone_number VARCHAR(11);
UPDATE students
SET  phone_number= 9856325895
WHERE student_id = 1;

UPDATE students
SET phone_number = 9658452158
WHERE student_id = 2;

UPDATE students
SET phone_number = 9874562554
WHERE student_id = 3;

UPDATE students
SET phone_number = 6589457125
WHERE student_id = 4;

UPDATE students
SET phone_number = 6874563214
WHERE student_id = 5;
ALTER TABLE courses
ADD COLUMN max_seats INT DEFAULT 60;
ALTER TABLE enrollments
ADD CONSTRAINT chk_grade
CHECK (grade IN ('A','B','C','D','F') OR grade IS NULL);
ALTER TABLE departments
CHANGE hod_name head_of_dept VARCHAR(100);
CREATE TABLE department_transfer_log (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    old_department_id INT,
    new_department_id INT,
    transfer_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
DELIMITER $$

CREATE PROCEDURE sp_enroll_student(
    IN p_student_id INT,
    IN p_course_id INT,
    IN p_enrollment_date DATE
)
BEGIN
    DECLARE v_exists INT DEFAULT 0;

    -- Check for duplicate enrollment
    SELECT COUNT(*) INTO v_exists 
    FROM enrollments 
    WHERE student_id = p_student_id AND course_id = p_course_id;

    IF v_exists > 0 THEN
        -- Raise a descriptive error if duplicate is found
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Duplicate Enrollment Error: This student is already enrolled in this course.';
    ELSE
        -- Insert the record if clear
        INSERT INTO enrollments (student_id, course_id, enrollment_date)
        VALUES (p_student_id, p_course_id, p_enrollment_date);
    END IF;
END $$

DELIMITER ;
USE college_db;

-- Clear it out if there's any partial remnant
DROP PROCEDURE IF EXISTS sp_transfer_student;

DELIMITER $$

CREATE PROCEDURE sp_transfer_student(
    IN p_student_id INT,
    IN p_new_dept_id INT
)
BEGIN
    DECLARE v_old_dept_id INT;
    
    -- Error Handler: Rollback on any SQL exception
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SELECT 'Transaction Failed! Everything was rolled back safely.' AS status_message;
    END;

    -- Fetch the current department ID before updating
    SELECT department_id INTO v_old_dept_id 
    FROM students 
    WHERE student_id = p_student_id;

    -- Start explicit transaction block
    START TRANSACTION;

        -- 1. Update student's department assignment
        UPDATE students 
        SET department_id = p_new_dept_id 
        WHERE student_id = p_student_id;

        -- 2. Log the administrative shift
        INSERT INTO department_transfer_log (student_id, old_department_id, new_department_id)
        VALUES (p_student_id, v_old_dept_id, p_new_dept_id);

    -- If both pass cleanly, commit changes permanently
    COMMIT;
    SELECT 'Transaction Completed Successfully!' AS status_message;
END $$

DELIMITER ;
CALL sp_transfer_student(1, 3);
EXPLAIN FORMAT=JSON 
SELECT s.first_name, s.last_name, c.course_name 
FROM enrollments e 
JOIN students s ON s.student_id = e.student_id 
JOIN courses c ON c.course_id = e.course_id 
WHERE s.enrollment_year = 2027;
USE college_db;

-- 51. Create a B-Tree index on students.enrollment_year
CREATE INDEX idx_student_enrollment_year ON students(enrollment_year);

-- 52. Create a composite UNIQUE index on enrollments(student_id, course_id)
-- Note: Your sample input data already has a duplicate entry (Enrollment ID 1 and 2 are duplicates!).
-- To prevent an "Error Code: 1062 - Duplicate entry" crash, we clean that duplicate out first.
DELETE FROM enrollments WHERE enrollment_id = 2;

CREATE UNIQUE INDEX uq_student_course ON enrollments(student_id, course_id);

-- 53. Create an index on courses.course_code
CREATE INDEX idx_course_code ON courses(course_code);
EXPLAIN FORMAT=JSON 
SELECT s.first_name, s.last_name, c.course_name 
FROM enrollments e 
JOIN students s ON s.student_id = e.student_id 
JOIN courses c ON c.course_id = e.course_id 
WHERE s.enrollment_year = 2027;

TASK 2: PERFORMANCE COMPARISON REPORT (INDEXES ACTIVE)

-- 55. MySQL Functional Index serving as a Partial Index for unevaluated grades
CREATE INDEX idx_partial_missing_grades 
ON enrollments ((CASE WHEN grade IS NULL THEN student_id END));
USE college_db;

SELECT e.enrollment_id, CONCAT(s.first_name, ' ', s.last_name) AS student_name, e.course_id
FROM enrollments e
INNER JOIN students s ON e.student_id = s.student_id;