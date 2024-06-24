# Git command

> git 기본 명령어를 정리해봅시다.

## init
- 현재 위치에 `.git` 폴더를 생성

```bash
git init
```

## add
- working directory => staging area


```bash
git add .
```


## status
- 현재 git 상태 확인

```bash
git status
```

## commit
- staging area에 올라간 내용을 스냅샷 찍기
    - `-m` 옵션을 통해 커밋메세지를 바로 입력가능

```bash
git commit -m "first commit"
```
