CREATE DATABASE COMPANY;
CREATE TABLE EMPLOYEE(
    ssn int PRIMARY KEY ,
    fname varchar(25),
    lname varchar(25),
    bdate date,
    Eaddress varchar(255),
    gender  CHAR(1),
    salary int,
    Dno	int NOT NULL
    );
CREATE TABLE DEPARTMENT(
    Dnumber int PRIMARY KEY,
    Dname varchar(25),               
    mgr_ssn int NOT NULL,
    mgr_start_date date
    );
CREATE TABLE PROJECT(
    Pnumber int PRIMARY KEY,
    Pname varchar(25),
    Plocation varchar(255),
    Dno int NOT NULL
    );
ALTER TABLE PROJECT ADD FOREIGN KEY (Dno)
REFERENCES DEPARTMENT(Dnumber);