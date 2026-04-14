-- ALTER
-- SERVER-VAR FOREIGN KEY CHECKS
-- ORACLE/POSTGRES: TRANSACTION BASED-DEFFER
-- BY DEFAULT DELETE... ON DELETE: CASCADE-UPDATE ?TOSEARCH
INSERT INTO EMPLOYEE (ssn, fname, lname, bdate, Eaddress, gender,salary,Dno)
VALUES (2, 'Tom', 'helmy', '2000-02-01','3773 Stracke Drive Suite 718\nEvelinemouth, MN 87950-4818', 'm','20200',100),
(3, 'elon', 'mask', '2000-04-22','2321 bakenham str, England', 'm','10000',103),
(4, 'patrick', 'star', '2000-08-30','4004 saint housse mere de dieu', 'f','3000',104);
-- If i insert the mgr ssn and the mgr wasn't in the department...logical error how to fix?
INSERT INTO DEPARTMENT (Dnumber,Dname, mgr_ssn, mgr_start_date)
VALUES (100, 'Compuo', 4, '2010-02-01'),
(103, 'hamada', 3, '2008-09-01'),
(104, 'lolz', 2, '2012-02-23');
INSERT INTO PROJECT (Pnumber,Pname,Plocation,Dno)
VALUES (34, 'elproj elgbar', 'elborg',100),
(54, 'blitz', 'italia',103),
(11, 'manhatten', 'elmarikh',104);
ALTER TABLE EMPLOYEE ADD FOREIGN KEY (Dno)
REFERENCES DEPARTMENT(Dnumber);
ALTER TABLE DEPARTMENT ADD FOREIGN KEY (mgr_ssn)
REFERENCES EMPLOYEE(ssn);