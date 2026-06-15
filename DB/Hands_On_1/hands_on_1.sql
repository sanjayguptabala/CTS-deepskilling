CREATE DATABASE college_db;


-- TASK 1: CREATE TABLES WITH MATCHING DATA TYPES


-- 1. Create departments table
CREATE TABLE departments (
    department_id INT AUTO_INCREMENT PRIMARY KEY, -- Fixed from SERIAL
    dept_name VARCHAR(100) NOT NULL,
    hod_name VARCHAR(100),
    budget DECIMAL(12,2)
);

-- 2. Create students table
CREATE TABLE students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    date_of_birth DATE,
    department_id INT, -- Perfectly matches parent table data type now
    enrollment_year INT,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

-- 3. Create courses table
CREATE TABLE courses (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    course_name VARCHAR(150) NOT NULL,
    course_code VARCHAR(20) UNIQUE,
    credits INT,
    department_id INT,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

-- 4. Create enrollments table
CREATE TABLE enrollments (
    enrollment_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    course_id INT,
    enrollment_date DATE,
    grade CHAR(2),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

-- 5. Create professors table
CREATE TABLE professors (
    professor_id INT AUTO_INCREMENT PRIMARY KEY,
    prof_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    department_id INT,
    salary DECIMAL(10,2),
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);


-- TASK 3: ALTER AND EXTEND THE SCHEMA 


-- 10. Add phone_number column
ALTER TABLE students ADD COLUMN phone_number VARCHAR(15);

-- 11. Add max_seats column [cite: 222]
ALTER TABLE courses ADD COLUMN max_seats INT DEFAULT 60;

-- 12. Add CHECK constraint [cite: 223]
ALTER TABLE enrollments ADD CONSTRAINT chk_grade CHECK (grade IN ('A', 'B', 'C', 'D', 'F') OR grade IS NULL);

-- 13. Rename hod_name to head_of_dept using explicit MySQL syntax 
ALTER TABLE departments CHANGE hod_name head_of_dept VARCHAR(100);

-- 14. Drop the phone_number column [cite: 226]
ALTER TABLE students DROP COLUMN phone_number;

SHOW TABLES;
DESCRIBE departments;
DESCRIBE courses;