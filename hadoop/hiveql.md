book data
============= 
*hive 실행 전 hadoop 항상 먼저 start
```
경로 ubunto@2-15~Hadoop어쩌구 sbin/start-all.sh
```
hive 실행
```
hiveserver2 --hiveconf hive.server2.thrift.port=10000 --hiveconf hive.root.logger=DEBUG,consol
```
새로운 터미널에서 beeline 실행
```
beeline
beeline> !connect jdbc:hive2://localhost:10000
```

기존 터미널에서 파일 하둡으로 가져오기
```
input 폴더 안에 books/users/book-ratings 파일 생성

hdfs dfs -mkdir input/Books
hdfs dfs -mkdir input/Users
hdfs dfs -mkdir input/Book_Ratings

하둡으로 dataset 파일 옮기기(경로 유의)

hdfs dfs -put ~/dmf/dataset/Books.csv input/Books/Books
hdfs dfs -put ~/dmf/dataset/Users.csv input/Users/Users
hdfs dfs -put ~/dmf/dataset/Book-Ratings.csv input/Book_Ratings/Book_Ratings

파일 삭제 방법
hdfs dfs -rm input/Books/Books.csv
hdfs dfs -rm input/Users/Users.csv
hdfs dfs -rm input/Book-Ratings

*폴더 삭제 시
-rm -r ~~~
```



(테이블 생성)
```
CREATE EXTERNAL TABLE Books (
    ISBN STRING,
    Title STRING,
    Author STRING,
    Year_Publication DATE,
    Publisher STRING,
    URL_S STRING,
    URL_M STRING,
    URL_L STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
    "separatorChar" = ";",  #구분 기준 ;
    "quoteChar"     = "\"", #csv 파일 내부 큰따옴표 삭제
    "escapeChar"    = "\\" 
)
STORED AS TEXTFILE
LOCATION '/user/ubunto/input/Books'
TBLPROPERTIES ('skip.header.line.count'='1');
```

(표 확인)
```
SELECT * FROM users_view LIMIT 10;
SELECT * FROM books_view LIMIT 10;
SELECT * FROM ratings_view LIMIT 10;
```

(삭제)
```
DROP TABLE ....;
DROP VIEWS ....;
```

(형변환 - VIEWS)
```
CREATE VIEW books_view AS
SELECT ISBN, Title, Author, CAST(Year_Publication AS INT) as year, Publisher
FROM books;
```


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