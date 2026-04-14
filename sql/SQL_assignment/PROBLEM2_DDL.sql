CREATE DATABASE Library_Management_System;
CREATE TABLE BOOK(
    book_id int AUTO_INCREMENT PRIMARY KEY ,
    title varchar(50),
    price int,
    pub_id	int,
    category_id int
    );
CREATE TABLE PUBLISHER(
    pub_id int PRIMARY KEY,
    pname varchar(255),
    paddress varchar(255)
    );
CREATE TABLE CATEGORY(
    category_id int AUTO_INCREMENT PRIMARY KEY ,
    catname varchar(25)
    );
CREATE TABLE MEMBER(
    member_id int PRIMARY KEY,
    Mname varchar(25),
    Maddress varchar(255),
    join_date datetime
    );
CREATE TABLE BORROWING_BOOK(
    member_id int,
    book_id int,
    borrow_date datetime ,
    due_date datetime,
    return_date datetime,
	PRIMARY KEY (member_id, book_id, borrow_date) 
    );
