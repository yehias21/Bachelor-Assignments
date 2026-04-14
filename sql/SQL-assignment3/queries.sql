-- Query 1
SELECT student_name FROM student WHERE level='SR'and student_id in(
    SELECT student_id FROM enrolled as e JOIN semester_course as sc 
    on e.quarter=sc.quarter and e.year=sc.year and
    e.course_code=sc.course_code WHERE sc.prof_id=1);

-- Query 2
SELECT MAX(age) FROM student WHERE major='History'or student_id in
	(SELECT student_id FROM enrolled as e JOIN semester_course as sc 
    on e.quarter=sc.quarter and e.year=sc.year and
    e.course_code=sc.course_code WHERE sc.prof_id IN
	(SELECT prof_id FROM Professor WHERE prof_name='Michael Miller'));

-- Query 3
SELECT DISTINCT s.student_name,c.name FROM student as s LEFT JOIN 
    (enrolled as e JOIN course as c on e.course_code=c.course_code)
    ON s.student_id=e.student_id;

-- Query 4
SELECT p.prof_name FROM Professor as p WHERE p.prof_id IN(
    SELECT sc.prof_id FROM semester_course as sc Left JOIN enrolled as e on e.quarter=sc.quarter and e.year=sc.year and
    e.course_code=sc.course_code 
	GROUP by sc.prof_id 
	Having COUNT(e.student_id)<5);

-- Query 5
SELECT s.student_name FROM student as s WHERE NOT EXISTS
	(SELECT sc.quarter,sc.course_code,sc.year FROM semester_course as sc WHERE sc.prof_id=2 AND
    NOT EXISTS (SELECT e.quarter,e.course_code,e.year
    FROM enrolled as e 
    WHERE e.student_id=s.student_id AND e.quarter=sc.quarter and e.year=sc.year and
    e.course_code=sc.course_code));

-- Query 6  
SELECT c.name FROM course as c WHERE course_code IN
(SELECT sc.course_code FROM semester_course as sc 
 where  sc.prof_id IN(
SELECT p.prof_id from Professor as p JOIN Department as d ON p.dept_id= d.dept_id 
WHERE d.dept_name='Computer Science')) 
OR NOT EXISTS(SELECT sc.course_code FROM semester_course as sc WHERE sc.course_code=c.course_code);

-- Query 7
Select s.student_name FROM student as s WHERE s.student_name LIKE 'M%' AND s.age<20 UNION
SELECT p.prof_name FROM Professor as p  WHERE p.prof_name LIKE 'M%' and p.prof_id in 
(SELECT sc.prof_id FROM semester_course as sc GROUP by sc.prof_id HAVING COUNT(*)>2);

-- Query 8  
SELECT p.prof_name FROM Professor as p  WHERE p.dept_id in (1,2,3,4) and p.prof_id not in 
(SELECT sc.prof_id FROM semester_course as sc GROUP by sc.prof_id HAVING COUNT(*)>=2);
-- Query 9  
    SELECT s.student_name,p.prof_name FROM enrolled as e JOIN semester_course as sc on e.quarter=sc.quarter
    and e.year=sc.year and e.course_code=sc.course_code RIGHT JOIN student as s on s.student_id=e.student_id 
    RIGHT JOIN Professor as p on p.prof_id=sc.prof_id UNION SELECT s.student_name,p.prof_name FROM enrolled as e 
    JOIN semester_course as sc on e.quarter=sc.quarter and e.year=sc.year and e.course_code=sc.course_code RIGHT 
    JOIN student as s on s.student_id=e.student_id LEFT JOIN Professor as p on p.prof_id=sc.prof_id;
-- Query 10
SELECT p.prof_name,sc.prof_id,sc.course_code,c.name FROM 
(semester_course as sc JOIN Professor AS p ON p.prof_id=sc.prof_id)
JOIN course as c ON c.course_code=sc.course_code 
GROUP BY sc.prof_id,sc.course_code 
HAVING COUNT(*)>1;
-- Query 11
SELECT d.dept_name FROM Department as d WHERE d.dept_id not in
( SELECT p.dept_id FROM Professor as p JOIN semester_course as sc on sc.prof_id=p.prof_id 
GROUP by p.dept_id HAVING COUNT(sc.course_code)>=3);
