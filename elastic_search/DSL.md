elastic search
============= 

## elasticsearch run

cd elasticsearch - > bin/elasticsearch
cd kibana -> bin/kibana

port -> localhost:5601


## _aliases
POST _aliases
```
{
  "actions": [
    {
      "add": {
        "index": "kibana_sample_data_ecommerce",
        "alias": "ecommerce"
      }
    }
  ]
}
```
 _aliases (데이터 이름에 별명 붙여주는 방식, 실제 이름이 바뀌는 것은 아님)

## QUERY DSL
```
{
  "size": 0, 
  //sql -> LIMIT
  "from": 0, 
  //OFFSET,
  "timeout": "1s",
  // sql에서 매칭되는 함수 X(실행 시간 제한)
  "_source": [], 
  // SELECT * FROM table_name  [] 비어있으면 * all, [] 안에 들어가면 해당 칼럼만 조건문,
  "query": {},
  // WHERE
  "aggs": {},
  // GROUP BY, COUNT, SUM..
  "sort": {},
  // ORDER BY
}
```
# 1. 검색

## term 검색

"term" -> 문자가 일치하는 친구 찾기

"terms" -> 여러 정보 부합하는 내용 검색할 때

"_source" -> 필요한 컬럼만 보고 찾고자 할 때

## match 검색
"match"  

예시 "products.product_name": "summer dark" 

-> summer or dark 
여러개의 토큰을 줬을 때 그 중 하나라도 맞으면 검색됨
(term은 토큰과 정확하게 맞는 검색)

"multi_match" -> 여러개의 필드 같이 검색 가능

여러개 조건 걸 때 -> "bool": { "must": [{}]}

"highlight" -> 골라진 문서 중에서 어디를 표시할까 / highlight라는 key값에 저장됨
```
        "highlight": {
          "products.product_name": [
            "Sweatshirt - <em>dark</em> blue",
            "Light jacket - <em>dark</em> blue"
          ]
        }
```

## sql

```
POST _sql?format=txt
{
  "query": """
  SELECT * FROM "TABLE"
  """
}
```

## suggest API


### 내부에서 직접적으로 사용할 수 있는 유사도 검사

"fuzziness" -> 유사도 숫자로 표시(단어의 순서에 따라 결정됨) 

ex) 1 => 단어 하나 의미(순서 or 스펠링) 

// 숫자가 높아질 수록 상관없는 단어


### suggest api 
#### term suggest - 추천 단어 제안 (오타 수정)
```
  "suggest": {
    "my_suggest": {
      "text": "pie",
      "term": {
        "field": "name"
      }
    }
```
// 편집거리 사용
4글자 이하는 검색 안됨 (defult 2)

pi X

appl -> appl, apple, app

stor -> store

*query가 없을 때 suggest 연동해서 사용하는 경우가 많음



#### comletion suggest - 자동 완성

"type": "completion"
```
  "suggest": {
    "my_suggest": {
      "prefix": "app",
      "completion": {
        "field": "name"
      }
      }
    }
```

# 2. 집계

SQL "GROUP BY" 랑 유사

기본구조
```
{ 
"query" : {},
"aggs": {}
}
```

"stats" -> count, min, max, avg, sum 다 보여줌

```
    "product_stat": {
      "count": 4675,
      "min": 6.98828125,
      "max": 2250,
      "avg": 75.05542864304813,
      "sum": 350884.12890625
    }
  }
 ```
"extended_stats" -> 제곱, 표준편차, 분산도 보여줌


"cardinality" -> 고유값 보여줌

"percentiles" -> 백분위 보여줌(숫자 데이터)
```
      "percentiles": {
        "field": "taxful_total_price",
        "percents": [
          1,
          5,
          25,
          50,
          75,
          95,
          99
        ]
      }
```
"geo_bounds" -> 위치 정보 경도, 위도 데이터 기준으로 집합(좌표가 포함된 하나의 박스를 그림)
결과
```
      "bounds": {
        "top_left": {
          "lat": 52.49999997206032,
          "lon": -118.20000001229346
        },
        "bottom_right": {
          "lat": 4.599999985657632,
          "lon": 55.299999956041574
        }
      }
```

## 버킷 집계
= GROUP BY (묶어서 다른 context 내에서 집계)

