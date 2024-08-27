Mapreduce
============= 
> ![alt text](image.png)

```
dataset > 대용량 파일

*가져오는 방법 : wget 링크
*zip 해제: unzip
*hadoop으로 이동: hdfs dfs -put input(이름)
```

1. mapper.py
```
예시)
import sys

for line in sys.stdin:
    line = line.strip()
    words = line.split()

    for word in words:
        print(f'{word}\t1')
```
```
에시2 - 정규표현식 이용)
import sys
import re # 정규표현식 사용하기 위한 코드 삽입

time_pattern = re.compile(r':(\d{2}):(\d{2}):(\d{2})')

# fstring 대신 r''사용
# \d = 숫자
# {2} = 두 자리
# email 정규표현식 예시 = '^[a-zA-Z0-9+-\_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

for line in sys.stdin:
    line = line.strip()
    # line.split(':')[1]

    match = time_pattern.search(line)

    if match:
        hour = match.group(1)
        print(f'{hour}\t1')
```

2. reducer.py
```
예시)
import sys

last_word = None
total_count = 0

for line in sys.stdin:
    line = line.strip()

    word, value = line.split('\t')
    value = int(value)

    if last_word == word:
        total_count += value
    else:
        if last_word is not None:
            print(f'{last_word}\t{total_count}')
        last_word = word
        total_count = value

if last_word == word:
    print(f'{last_word}\t{total_count}')
```

3. linux환경에서 실행
```
cat (파일 이름) | python3 mapper.py | sort | python3 reducer.py
```


4. hadoop에서 실행
```
hadoop jar ~/hadoop-3.3.6/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar \
-input /user/ubunto(오타)/input/파일이름 \
-output /user/ubunto(오타)/output/이름(생성) \
-mapper 'python3 /home/ubunto(오타)/dmf/hadoop/폴더이름/mapper.py' \
-reducer 'python3 /home/ubunto(오타)/dmf/hadoop/폴더이름/reducer.py'
```
-> 결과 확인 localhost:9870 output 
