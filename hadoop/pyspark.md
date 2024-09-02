pyspark
============= 

1. 설치
```
wget https://dlcdn.apache.org/spark/spark-3.5.2/spark-3.5.2-bin-hadoop3.tgz
```

2. 코드 실행
```
spark-submit (파일 이름)
```

## 1. wordcount.py 작성
```
from pyspark import SparkContext
```

- sc 변수 선언(sparkcontext의 약자)


#### spark 속성 설정
SparkConf()

```
# local 말고 hadoop에 연결되어 있는 파일 읽기 위한 코드

from pyspark import SparkConf

conf = SparkConf().setMaster('yarn')
```

### HDFS에서 파일 읽기
```
file_path = 'hdfs://localhost:9000/user/ubuntu/input/input.txt'
lines = sc.textFile(file_path)
```

### local에서 파일 읽기
```
file_path = '/home/ubuntu/dmf/spark/0.RDD/input.txt'
lines = sc.textFile(file_path)
```

## 2. log_rdd.py 작성
1. local에서 access.log 파일 읽기(8월1일 log)
```
from pyspark import SparkContext

sc = SparkContext()

file_path = 'file:///home/ubunto/dmf/spark/0.RDD/access.log'
lines = sc.textFile(file_path)
```

2. 한 줄씩 log 데이터 자르기 (lambda함수)
```
mapped_lines = lines.map(lambda line: line.split())
```

### foreach 함수
- print함수 안에 한 줄, 한 줄 데이터 넣는 효과(java에서도 동일)

```
mapped_lines.foreach(print)
```

3. filter
- 필터링
```
python에서 filter함수 -> filter(function, list)
spark에서 사용법 -> list.filter(function)
```

3-1) 4xx 코드 출력
```
def filter_4xx(line):
    return line[6][0] == '4'

filterd_lines = mapped_lines.filter(filter_4xx)
filterd_lines.foreach(print)
```
3-2) POST & /product 코드 출력
```
def filter_post_product(line):
    return line[3] == '"POST' and 'product' in line[4]

filterd_log = mapped_lines.filter(filter_post_product)
filterd_log.foreach(print)
```

4. reduce
4-1) method(post, get) 별 요청 수
```
method_rdd = mapped_lines.map(lambda line: (line[3], 1)) \
    .reduceByKey(lambda a, b: a+b)
method_rdd.foreach(print)
```
```
# mapped_lines.map 결과값 ('"GET', 1) ('"POST', 1) ....
# .reduceByKey() 결과값 : ('"GET', 925)('"POST', 926)
```

4-2) 시간대별 요청 수
```
time_rdd = mapped_lines.map(lambda line: (line[2].split(':')[0], 1)) \
    .reduceByKey(lambda a, b: a+b)
time_rdd.foreach(print)
```
```
# 결과값 ('03', 78) ('05', 78) ('06', 60) ('07', 75)....
```
5. groupby
5-1) status code, api method 별 ip리스트 출력
```
def code_method(line):
    ip = line[0]
    status = line[6]
    method = line[3].replace('"', '') #"를 비어있는 문자열로 바꾸는 python 함수 : replace
    return (status, method), ip

group_by_rdd = mapped_lines.map(code_method)
group_by_rdd.foreach(print)
```
```
# 결과값 
(('400', 'GET'), '157.132.14.186')
(('301', 'POST'), '101.107.177.60')
...
````