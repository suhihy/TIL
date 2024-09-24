elastic search
============= 

# 1. basic
## 1-1 create index (PUT)
### index를 만들지 않은 상태로 문서 생성

```
PUT /test/_doc/1
{
    "title": "this is title",
    "content": "this is content",
    "year": 2024
}

GET /test

```

### 인덱스 생성(mapping)
```
PUT /movie
{
    "mappings": {
        "properties": {
            "movieNm": {
                "type": "text"
            },
            "year": {
                "type": "integer"
            },
            "date": {
                "type": "date"
            }
        }
    }
}

GET /movie
```

## 1-2 document (POST)
```
POST /movie/_doc/1
{
    "movieNm": "superman",
    "year": 2024,
    "date": "2024-01-01"
}

POST /movie/_doc/1
{
    "movieNm": "0000",
    "year": 2024,
    "date": "2024-00-00"
}

... 반복해서 생성 가능
```

## 1-3 search (_search)

### search data
```
GET /movie/_search
```

### url 방식 검색
```
GET /movie/_search?q=2024
GET /movie/_search?q=spiderman

GET /movie/_search?q=
```

### request body 방식 검색
```
POST /movie/_search
{
    "query": {
        "term": {
            "year": {
                "value": "2021"
            }
        }
    }
}

POST /movie/_search
{
    "query": {
        "term": {
            "movieNm": {
                "value": "superman"
            }
        }
    }
}
```

### aggregation(집계)
```
POST /movie/_search
{
    "aggs": {
        "total-count": {
            "terms": {
                "field": "year"
            }
        }
    }
}
```

# 2. data modeling

## 2-1 mapping

### 모델링 (table 만드는 것 - column 정의)
```
PUT /movie
{
    "mappings": {
        "properties": {
            "title": {
                "type": "text"
            },
            "content": {
                "type": "text"
            }
        }
    }
}
```

### 데이터 추가
```
POST /movie/_doc
{
    "title": "title2",
    "content": "content2"
}
```

### 모든 데이터 조회
```
GET /movie/_search
```

### mapping 정보 확인
```
GET /movie
```

### index close, open
```
POST /movie/_close
POST /movie/_open
```

### index 삭제 (DELETE)
```
DELETE /movie
```

### add mapping (_mapping)
```
PUT /movie/_mapping
{
    "properties": {
        "year": {
            "type": "integer"
        }
    }
}
```

### add document
```
POST /movie/_doc
{
    "title": "슈퍼맨",
    "content": "재밌습니다",
    "year": 2024
}

GET /movie/_search
```

### 재색인(_reindex)

#### 인덱스 복제
```
POST _reindex
{
    "source": {
        "index": "movie"
    },
    "dest": {
        "index": "movie.v2"
    }
}

GET /movie.vs/_search
```

#### 인덱스 복제(특정 필드만)
```
POST _reindex
{
    "source": {
        "index": ["title", "content"]
    },
    "dest": "movie.v3"
}

GET /movie.v3/_search
```

## 2-2 CRUD

### id 부여하는 경우
```
POST /movie/_doc/1
{
    "title": iron-man",
    "content": "iron"
}
```

### id가 없는 경우 -> UUID를 자동으로 생성
```
POST /movie/_doc
{
    "title": "iron-man",
    "content": "iron"
}
```

### 하나의 필드만 넣는 경우 -> 덮어 씌워짐
```
PUT /movie/_doc/1
{
    "title": "iron-man 2"
}
```

### 특정 필드만 수정하는 경우
```
POST /movie/_update/ACH......
{
    "doc": {
        "title": "iron-man 3"
    }
}

DELETE /movie/_doc/1
```

## 2-3 bulk
```
POST /_bulk
{"index":{"_index":"test", "_id":"1"}}
{"field":"value one"}
{"index":{"_index":"test", "_id":"2"}}
{"field":"value two"}
```

### 여러 데이터 수정 (_update_by_query)
```
POST /movie/_update_by_query
{
    "script": {
        "source": "ctx._source.title = 'test'",
        "lang": "painless"
    },
    "query": {
        "term": {
            "year": {
                "value": 2021
            }
        }
    }
}
```

### 여러 데이터 삭제 (_delete_by_query)
POST /movie/_delete_by_query
{
    "query": {
        "term": {
            "year": {
                "value": "2021"
            }
        }
    }
}


# 3. data type

## 3-1 문자

### keyword type
=> 분석기를 사용하지 않음

```
PUt /book
{
    "mappings": {
        "properties": {
            "title": {
                "type": "keyword"
            }
        }

    }
}

POST /book/_doc
{
    "title": "hello"
}

POST /book/_doc
{
    "title": "HELLO"
}

GET /book/_search

POST /book/_search
{
    "query": {
        "term": {
            "title": {
                "value": "HELLO"
            }
        }
    }
}

DELETE /book

PUT /book
{
  "mappings": {
    "properties": {
      "title": {
        "type": "keyword"
      },
      "content": {
        "type": "text"
      }
    }
  }
}

GET /book

POST /book/_doc
{
  "title": "hello world",
  "content": "good book"
}

POST /book/_doc
{
  "title": "hello python",
  "content": "good python!!!"
}

POST /book/_doc
{
  "title": "hello elastic",
  "content": "bad book!!!"
}

GET /book/_search
```

### keyword 타입은 완전히 일치해야 검색됨
```
GET /book/_search
{
  "query": {
    "term": {
      "title": {
        "value": "hello world"
      }
    }
  }
}
```

### text는 분석기를 통해 나눠진 토큰과 일치하면 검색됨
```
GET /book/_search
{
  "query": {
    "term": {
      "content": {
        "value": "!"
      }
    }
  }
}

POST _analyze
{
  "analyzer": "standard",
  "text": "bad book!!!!!",
  "explain": true
}
```
## 3-2 date type
```
PUT /post
{
  "mappings": {
    "properties": {
      "date": {
        "type": "date"
      }
    }
  }
}

POST /post/_doc
{
  "date": "2024-09-24"
}

POST /post/_doc
{
  "date": "2024-09-24T12:10:10Z"
}

POST /post/_doc
{
  "date": "12367812424"
}

GET /post/_search

DELETE /post

PUT /post
{
  "mappings": {
    "properties": {
      "date": {
        "type": "date",
        "format": "yyyy-MM-dd||yyyy/MM/dd"
      }
    }
  }
}

POST /post/_doc
{
  "date": "2024/09/24"
}

POST /post/_doc
{
  "date": "2024-09-01"
}

GET /post/_search
{
  "sort": [
    {
      "date": {
        "order": "desc"
      }
    }
  ]
}
```

## 3-3 range type
```
PUT /range_index
{
  "mappings": {
    "properties": {
      "my_int_range": {
        "type": "integer_range"
      },
      "my_date_range": {
        "type": "date_range"
      }
    }
  }
}

POST /range_index/_doc
{
  "my_int_range": {
    "gte": 10,
    "lt": 20
  },
  "my_date_range": {
    "gte": "2024-01-01",
    "lt": "2024-07-01"
  }
}

GET /range_index/_search
{
  "query": {
    "term": {
      "my_int_range": {
        "value": 25
      }
    }
  }
}

GET /range_index/_search
{
  "query": {
    "term": {
      "my_date_range": {
        "value": "2024-12-05"
      }
    }
  }
}

# within, contains, intersects
GET /range_index/_search
{
  "query": {
    "range": {
      "my_int_range": {
        "gte": 9,
        "lte": 30,
        "relation": "within"
      }
    }
  }
}
```


