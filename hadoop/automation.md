automation
============= 

## CRON 

 * (>>) 왼쪽에 있는 결과물을 오른쪽 파일에 저장해주세요/ 기존 데이터 유지. 덧붙이기
* (>) 새로운 데이터로 덮어씌우기

### 반복작업 수행 : cron

```
crontab -e
```
choose 2
i (insert 모드)

```
*****(=매 분, 매 시간, 매 일, 매 월, 매 주마다 실행해주세요) /home/ubunto/dmf/automation/test.log(파일 위치)

**30**(30일마다)

****0(매 주 일요일마다)

```
```
esc(insert 모드 멈추기)
:wq(bash로 돌아오기)

sh test.sh(코드 실행)
```

------------
~/hadoop-3.3.6/sbin/start-all.sh (하둡 실행)

## 0.log_generate.py

pip 먼저 다운로드(max북은 필요X)
```
sudo apt-get install python3-pip
```

faker 사용해 난수(log) 생성
```
pip3 install faker
```

* log_line 
= 94.49.94.23(랜덤한 4자리 수) - [날짜 시간] - (경로GET/POST 등....) 형식의 랜덤한 값 생성 시도

ex) 2.4.154.77 "POST /index HTTP/1.1" 400 483

~자세한 코드는....파일 코드 참고
[0.log_generate.py](/hadoop/automation/0.log_generate.py)


ls - l (권환 확인 코드)
* 2진수로 표시
r(2*2)w(2)-(0)  = 6

```
chmod +x test.sh
(test.sh에게 x라는 실행 권한 주기)
```

timedelta -> dday 셀 때 시간 계산 가능하도록 돕는

for _ => i(반복문 돌리기 위한 index) 값 사용 안 할 때


## 1.log_file_to_hdfs.py
> 하둡에 log 결과값 업로드
python으로 작성

- 라이브러리 사용
HdfsCLI 참고
https://hdfscli.readthedocs.io/en/latest/

```
pip3 install hdfs
```

ls 명령어랑 똑같은 역할 = os.listdir

~자세한 코드는....파일 코드 참고
[1.log_file_to_hdfs.py](/hadoop/automation/1.log_file_to_hdfs.py)

## 2.hiveQL.py
>hive로 데이터 처리

hive 실행....코드 0827 코드 참고

>스키마 schema
```
CREATE EXTERNAL TABLE IF NOT EXISTS logs (
    ip_address STRING,               -- IP 주소
    log_timestamp STRING,            -- 로그 타임스탬프 (날짜 및 시간)
    http_method STRING,              -- HTTP 메소드 (GET, POST, PUT, DELETE)
    request_path STRING,             -- 요청 경로 (URI)
    protocol STRING,                 -- 프로토콜 (HTTP 버전)
    status_code INT,                 -- HTTP 상태 코드
    response_size INT                -- 응답 크기 (바이트)
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.RegexSerDe'
WITH SERDEPROPERTIES (
    "input.regex" = "^(\\S+) \\[(\\S+ \\S+)\\] \\\"(\\S+) (\\S+) (\\S+)\\\" (\\d+) (\\d+)$"
)
STORED AS TEXTFILE
LOCATION 'input/logs';
```

* 정규표현식 - ^(\\S+) \\[(\\S+ \\S+)\\] \\\"(\\S+) (\\S+) (\\S+)\\\" (\\d+) (\\d+)$

*S+ -> 문자열 여러개 \
*\ -> 빈칸 \
*d+ -> 숫자


```
select * from logs limit 10;
```

- hive python으로 사용하기 위한 라이브러리
PyHive
https://pypi.org/project/PyHive/


다운받는 코드
```
pip3 install pyhive
pip3 install thrift thrift-sasl
```

~자세한 코드는....파일 코드 참고
[2.hiveQL.py](/hadoop/automation/2.hiveQL.py)