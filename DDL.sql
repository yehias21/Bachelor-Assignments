CREATE TABLE Department (
    dept_id INT PRIMARY KEY, 
    dept_name VARCHAR(50));

CREATE TABLE student (
    student_id INT PRIMARY KEY, 
    student_name VARCHAR(50), 
    major  VARCHAR(50), 
    `level` VARCHAR(2), 
    age INT);

CREATE TABLE Professor (
    prof_id INT PRIMARY KEY , 
    prof_name VARCHAR(50), 
    dept_id INT,
    CONSTRAINT prof_dept_id FOREIGN KEY (dept_id) REFERENCES Department(dept_id));

CREATE TABLE course (
    course_code VARCHAR(4)  PRIMARY KEY, 
    `name`  VARCHAR(50));

CREATE TABLE semester_course (
    course_code VARCHAR(4), 
    quarter  VARCHAR(6), 
    year INT, 
    prof_id INT,
    PRIMARY KEY(course_code,quarter,year),
    CONSTRAINT sc_course_code FOREIGN KEY (course_code) REFERENCES course(course_code),
    CONSTRAINT sc_prof_id FOREIGN KEY (prof_id) REFERENCES Professor(prof_id)
    );

CREATE TABLE enrolled (
    student_id INT, 
    course_code VARCHAR(4), 
    quarter VARCHAR(6), 
    year INT, 
    enrolled_at DATE,
    PRIMARY Key(course_code,quarter,year,student_id),
    CONSTRAINT enrolled_FK FOREIGN KEY (course_code,quarter,year) REFERENCES semester_course(course_code,quarter,year)
);
