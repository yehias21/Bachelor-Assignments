SELECT Mname FROM MEMBER WHERE join_date>='2000-09-01';
SELECT * FROM MEMBER WHERE join_date>='1995-10-01' and join_date< '2019-10-02';
SELECT * FROM BOOK WHERE (price>=15 and price<= 20) or pub_id in (SELECT pub_id FROM PUBLISHER WHERE pname='Oxford');
SELECT title FROM BOOK WHERE book_id in (SELECT book_id FROM BORROWING_BOOK WHERE member_id in(SELECT member_id FROM MEMBER WHERE Mname='Scot Reinger'));
SELECT Mname from MEMBER where member_id in (SELECT member_id FROM BORROWING_BOOK WHERE borrow_date>='2019-01-01'and borrow_date<'2020-01-01'
);