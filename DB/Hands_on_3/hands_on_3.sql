-- TASK 1: SUBQUERIES

SELECT student_id, COUNT(course_id) AS enrollment_count
FROM enrollments
GROUP BY student_id
HAVING COUNT(course_id) > (
    SELECT AVG(enr_count) 
    FROM (
        SELECT COUNT(course_id) AS enr_count 
        FROM enrollments 
        GROUP BY student_id
    ) AS sub_counts
);

SELECT course_id, course_name 
FROM courses c
WHERE NOT EXISTS (
    SELECT 1 
    FROM enrollments e 
    WHERE e.course_id = c.course_id 
      AND (e.grade != 'A' OR e.grade IS NULL)
) AND EXISTS (
    SELECT 1 
    FROM enrollments e 
    WHERE e.course_id = c.course_id
);

SELECT p1.professor_id, p1.prof_name, p1.department_id, p1.salary
FROM professors p1
WHERE p1.salary = (
    SELECT MAX(p2.salary) 
    FROM professors p2 
    WHERE p2.department_id = p1.department_id
);

SELECT d.dept_name, dept_summary.avg_salary
FROM (
    SELECT department_id, AVG(salary) AS avg_salary 
    FROM professors 
    GROUP BY department_id
) AS dept_summary
JOIN departments d ON d.department_id = dept_summary.department_id
WHERE dept_summary.avg_salary > 85000.00;

-- TASK 2: CREATING AND USING VIEWS 

CREATE OR REPLACE VIEW vw_student_enrollment_summary AS
SELECT 
    CONCAT(s.first_name, ' ', s.last_name) AS full_name,
    d.dept_name,
    COUNT(e.course_id) AS courses_enrolled,
    AVG(CASE 
        WHEN e.grade = 'A' THEN 4
        WHEN e.grade = 'B' THEN 3
        WHEN e.grade = 'C' THEN 2
        WHEN e.grade = 'D' THEN 1
        WHEN e.grade = 'F' THEN 0
        ELSE NULL 
    END) AS gpa
FROM students s
LEFT JOIN departments d ON s.department_id = d.department_id
LEFT JOIN enrollments e ON s.student_id = e.student_id
GROUP BY s.student_id, s.first_name, s.last_name, d.dept_name;

CREATE OR REPLACE VIEW vw_course_stats AS
SELECT 
    c.course_name,
    c.course_code,
    COUNT(e.enrollment_id) AS total_enrollments,
    AVG(CASE 
        WHEN e.grade = 'A' THEN 4
        WHEN e.grade = 'B' THEN 3
        WHEN e.grade = 'C' THEN 2
        WHEN e.grade = 'D' THEN 1
        WHEN e.grade = 'F' THEN 0
        ELSE NULL 
    END) AS avg_gpa
FROM courses c
LEFT JOIN enrollments e ON c.course_id = e.course_id
GROUP BY c.course_id, c.course_name, c.course_code;

SELECT * FROM vw_student_enrollment_summary WHERE gpa > 3.0;

CREATE OR REPLACE VIEW vw_students_2022_subset AS
SELECT student_id, first_name, last_name, email, enrollment_year
FROM students
WHERE enrollment_year = 2022
WITH CHECK OPTION;

-- TASK 3: STORED PROCEDURES AND TRANSACTIONS

DROP TABLE IF EXISTS department_transfer_log;
DROP PROCEDURE IF EXISTS sp_enroll_student;
DROP PROCEDURE IF EXISTS sp_transfer_student;
DROP PROCEDURE IF EXISTS sp_savepoint_test;

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
    IF EXISTS (SELECT 1 FROM enrollments WHERE student_id = p_student_id AND course_id = p_course_id) THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Duplicate enrollment error: Student is already registered for this course.';
    ELSE
        INSERT INTO enrollments (student_id, course_id, enrollment_date, grade)
        VALUES (p_student_id, p_course_id, p_enrollment_date, NULL);
    END IF;
END$$

CREATE PROCEDURE sp_transfer_student(
    IN p_student_id INT,
    IN p_new_dept_id INT
)
BEGIN
    DECLARE v_old_dept_id INT;
    
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;
    
    SELECT department_id INTO v_old_dept_id FROM students WHERE student_id = p_student_id;
    
    UPDATE students SET department_id = p_new_dept_id WHERE student_id = p_student_id;
    
    INSERT INTO department_transfer_log (student_id, old_department_id, new_department_id)
    VALUES (p_student_id, v_old_dept_id, p_new_dept_id);
    
    COMMIT;
END$$

CREATE PROCEDURE sp_savepoint_test()
BEGIN
    START TRANSACTION;
    
    INSERT INTO enrollments (student_id, course_id, enrollment_date, grade) 
    VALUES (1, 3, '2026-06-22', 'A');
    
    SAVEPOINT after_first_insert; 
    
    BEGIN
        DECLARE CONTINUE HANDLER FOR SQLEXCEPTION 
        BEGIN
            ROLLBACK TO after_first_insert;
        END;
        
        INSERT INTO enrollments (student_id, course_id, enrollment_date, grade) 
        VALUES (999, 999, '2026-06-22', 'F'); 
    END;
    
    COMMIT;
END$$

DELIMITER ;