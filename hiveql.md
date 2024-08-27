book data
============= 
1. Books 테이블에서 중복된 ISBN 확인

SELECT
ISBN,
COUNT(ISBN)
FROM Books
GROUP BY ISBN,
HAVING COUNT(ISBN) > 1;

2. Ratings 테이블에서 중복된 사용자-책 평가 확인

SELECT
ISBN, ID,
COUNT(ISBN)
FROM Book_Ratings
GROUP BY ISBN, ID
ORDER BY ISBN DESC
LIMIT 10;

3. Users 테이블에서 Age의 결측값 확인

SELECT  
COUNT(*)-COUNT(Age)
FROM users_view;

4. Books 테이블에서 Year_Of_Publication의 결측값 확인

SELECT COUNT(*) FROM books_view WHERE year IS NULL;

5. 사용자 연령의 기초 통계(최소, 최대, 평균)를 확인합니다.

USers- Age
min, max, avg

SELECT MAX(Age), MIN(Age), AVG(Age) FROM users_view;

6. 책의 출판 연도에 대한 기초 통계(최소, 최대, 평균)를 확인합니다.

SELECT MAX(year) as max, MIN(year) as min, AVG(year) as avg FROM books_view;

7. 평점의 분포 확인

SELECT rating, COUNT(*)
FROM ratings_view
GROUP BY rating;

8. 출판사별 책 수 및 평균 평점

publisher -> count, 평점(rating)
books_view / ratings_view 두 개 표 결합 필요

SELECT b.publisher, COUNT(*) as count, AVG(r.rating) as rating
FROM books_view b
JOIN ratings_view r
ON b.ISBN = r.ISBN
GROUP BY b.publisher
ORDER BY count DESC
LIMIT 10;

9. 가장 많이 평가된 책과 그 평점

books_view
ratings_view 

SELECT b.Title, COUNT(r.rating) as count, AVG(r.rating) as rating
FROM books_view b
JOIN ratings_view r
ON b.ISBN = r.ISBN
GROUP BY b.Title
ORDER BY count DESC
LIMIT 10;

10. 책의 출판 연도와 평점 간의 관계를 확인합니다.

출판연도 기준으로 내림차순
-> ISBN 으로 결합해서 AVG(r.rating)

SELECT b.year, AVG(r.rating) as rating
FROM books_view b
JOIN ratings_view r
ON b.ISBN = r.ISBN
GROUP BY b.year
ORDER BY b.year DESC;

11. 사용자 위치별 평점 차이

users_view - Location
ratings_veiw - rating

SELECT u.Location, AVG(r.rating) as rating, COUNT(r.rating) as rating_count
FROM users_view u
JOIN ratings_view r
ON u.ID = r.ID
GROUP BY u.Location
HAVING COUNT(r.rating) > 10
ORDER BY AVG(r.rating) DESC
LIMIT 10;

12. 각 저자별로 평균 평점이 어떻게 다른지 확인합니다. 적어도 10개 이상의 평가를 한 경우만 출력합니다.

SELECT b.Author, AVG(r.rating) as rating, COUNT(r.rating) as rating_count
FROM books_view b
JOIN ratings_view r
ON b.ISBN = r.ISBN
GROUP BY b.Author
HAVING COUNT(r.rating) > 10
ORDER BY AVG(r.rating) DESC
LIMIT 10;

13. 평점 상위 10개의 책이 어느 연도에 많이 출판되었는지 확인합니다.

상위 10개의 책 연도 찾기,,,!!

WITH TopBooks AS (
SELECT 
b.year,
b.ISBN,
AVG(r.rating) as rating
FROM 
books_view b
JOIN 
ratings_view r
ON 
b.ISBN = r.ISBN
GROUP BY b.ISBN, b.year
HAVING COUNT(r.rating) > 10
ORDER BY 
AVG(r.rating) DESC
LIMIT 10
)
SELECT
t.year,
COUNT(t.year) AS number_of_books
FROM
TopBooks t
GROUP BY t.year
ORDER BY 
number_of_books DESC;