
---

# Git 정리

## Shell과 CLI

* **Shell**: 운영체제의 커널과 사용자를 이어주는 소프트웨어

  * 종류: `sh`, `csh`, `bash`, `zsh`
* **CLI (Command Line Interface)**: 명령어 기반 인터페이스
* **GUI (Graphic User Interface)**: 그래픽 기반 인터페이스 (일반 사용자 친숙)

---

## 버전 관리

### 버전 관리 도구 형태

1. **로컬(Local)**: 개인 PC에서만 관리
2. **중앙 집중식(Centralized)**: 중앙 서버에서 버전 관리 (SVN 등)
3. **분산(Distributed)**: 모든 개발자가 버전 전체를 복제 (Git)

---

## Git이란?

* **분산 버전 관리 시스템**
* 리누스 토발즈와 다른 커널 개발자가 개발 (2005년, 리눅스 커널 개발용)
* 무료, 오픈소스
* 모든 OS 지원
* 사실상 업계 표준

---

## Git의 특징

* 작고 빠르다
* 변경 이력 추적
* 브랜치와 머지
* 분산 버전 관리
* 로컬에서도 과거 이력 관리 가능

---

## Git 버전 관리 개념

* **워킹 디렉토리**: 실제 작업 중인 디렉토리
* **스테이징 영역 (Index/Stage)**: 커밋 전 임시 저장소
* **Git 디렉토리 (.git)**: 버전 정보 저장소

### 버전 관리 흐름

1. **Modified**: 파일 수정됨
2. **Staged**: 스테이징 영역에 추가됨
3. **Committed**: Git DB에 저장됨

---

## Git 내부 객체

* **Blob**: 파일의 내용 자체 (binary large object)
* **Tree**: 디렉토리 구조 및 메타데이터
* **Commit**: 특정 시점의 스냅샷 + 메타데이터 (작성자, 메시지 등)

---

## Git 기본 명령어

### 설정

```bash
vi ~/.gitconfig         # 내 아이디/이메일 확인 및 수정
git config --global user.name "이름"
git config --global user.email "이메일"
```

### 저장소 관련

```bash
git init                # 지역 저장소 생성
git clone <주소>        # 원격 저장소 복제
git remote add origin <주소>   # 원격 저장소 등록
git remote -v           # 원격 저장소 확인
```

### 변경 관리

```bash
git status              # 상태 확인
git add <파일명>        # 스테이징
git commit -m "메시지"  # 커밋
git reset <옵션>        # 되돌리기
```

### 로그

```bash
git log                 # 전체 로그
git log -1              # 최근 1개
git log --pretty=oneline # 한 줄 출력
```

---

## Git 브랜치 관련 명령

```bash
git branch                  # 브랜치 목록 확인
git branch <브랜치명>       # 브랜치 생성
git branch -d <브랜치명>    # 브랜치 삭제

git checkout <브랜치명>     # 브랜치 이동
git checkout -b <브랜치명>  # 브랜치 생성 + 이동

git switch <브랜치명>       # 브랜치 이동 (최신 권장)
git merge <브랜치명>        # 브랜치 병합
```

---

## 커밋 관련

* **수정하기**: `git commit --amend`
* **취소하기**: `git reset HEAD^`
* **되돌리기**: `git revert HEAD`
* **가져오기**: `git cherry-pick <커밋ID>`

---

## Git 원격 저장소

```bash
git fetch    # 원격 변경 사항 가져오기 (병합 X)
git pull     # 원격 변경 사항 가져오기 (병합 O)
git push     # 원격 저장소로 업로드
```

---

## 충돌 해결

1. 충돌 파일에서 `<<<<<<<`, `=======`, `>>>>>>>` 확인
2. 수정 후

   ```bash
   git add <파일명>
   git commit
   ```

---

## 파일 이동 / 이름 변경

```bash
mv ../main.md <하위 디렉토리>
mv bin/main.md .          # 현재 디렉토리로 이동
mv *.md bin               # 모든 .md 이동
mv test.md test_rename.md # 이름 변경
mv test.md bin/rename.md  # 이동 + 이름 변경
```

---

## 협업 시 커밋 메시지 컨벤션

* `feat`: 기능 개발 관련
* `fix`: 오류 개선, 버그 패치
* `docs`: 문서화
* `test`: 테스트 관련
* `conf`: 환경 설정 관련
* `build`: 빌드 관련

---

## Pre-commit Hook

```bash
pre-commit sample-config > .pre-commit-config.yaml
pre-commit run
```

---

## 주요 용어

* **main**: 기본 브랜치 이름
* **origin**: 원격 저장소 기본 이름
* **HEAD**: 현재 작업 중인 커밋을 가리키는 포인터

---

## GUI 도구

* GitKraken
* SourceTree
* GitHub Desktop

---
 
