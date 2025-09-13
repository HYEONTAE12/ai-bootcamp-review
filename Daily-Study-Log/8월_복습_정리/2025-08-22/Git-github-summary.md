# 오늘 배운 Git/GitHub 정리

## 1) Merge vs Rebase

### 🔹 **merge commit 인커젼 상태**

* **상황**: 다른 사람이 작업한 게 **지금은 필요 없다** → **나중에 합치기**
* **전략**: **merge**로 해결 (이력 보존, 충돌 생기면 그때 해결)

### 🔹 **rebase**

* **상황**: 다른 사람이 작업한 게 **지금 필요** → 내 브랜치를 최신 이력 위로 **재배치**
* **절차**

  ```bash
  git fetch origin
  git rebase origin/main   # 또는 rebase 대상 브랜치
  # 충돌 해결 후
  git add .
  git rebase --continue    # rebase 완료 후 continue까지 완료해야함
  ```
* 필요 시 중단/취소: `git rebase --abort`

### 🔹 GitHub에서 파일을 직접 수정한 경우(push가 안 됨)

* **원인**: 원격(깃허브) 이력이 앞섬 → 로컬과 **이력 불일치**
* **해결**

  ```bash
  git pull --rebase origin main   # 권장
  # 또는
  git fetch origin && git merge origin/main
  # 이후
  git push
  ```

---

## 2) 브랜치/배포 모델

### ✅ **git flow**

* 가장 전통적이고 많이 쓰이는 모델
* 각 단계가 명확히 구분되어 **주기적 배포**에 유리, **복잡**함
* 주요 브랜치: `master`, `develop` (+ 배포 release/hotfix 브랜치 존재)

### ✅ **github flow**

* **브랜치 모델 단순화**
* **CI 의존성** 높음, **Pull request가 중요**
* PR이 없으면 실수 대응이 어려움

### ✅ **gitlab flow**

* (개요) GitLab 권장 방식. 환경별 브랜치/이슈 중심 흐름(세부는 팀 정책에 맞춤)

---

## 3) GitHub 협업 요소

### **issues**

* 질문, 개발 포지션, 문제 해결 등 트래킹

### **Pull requests**

* 메인 코드 반영 요청, 코드 리뷰, 최종 컨펌
* **Pull request 가 중요하다**

---

## 4) Conventional Commits (커밋 메시지 타입)

* `feat`: 기능 개발 관련
* `fix`: 오류 개선 혹은 버그 패치
* `docs`: 문서화 작업
* `test`: test 관련
* `conf`: 환경설정 관련 *(작성 내용 유지)*
* `build`: 빌드 작업 관련
* `ci`: Continuous Integration 관련
* `chore`: 패키지 매니저, 스크립트 등
* `style`: 코드 포매팅 관련
* `refactor`: 구조 개선

### 예시 1

```
{type}: {description} 작업단위 축약(breaking change가 있다면 type 뒤에 !)

{body} 작업 상세 기술

{footer} 부가정보(ex) BREAKING CHANGE: Drop email sign up support)
```

### 예시 2

```
feat: add sign up component

This commit adds the sign up component to the application.

Closes #123
```

### 예시 3

```
fix!: resolve issue with login page

This commit fixes an issue with the login page that prevented users from
logging in.

Closes #123
BREAKING CHANGE: drop social login support
```

---

## 5) Stash (작업 잠시 미루기)

```bash
git stash            # 또는: git stash save "{메모}"
git stash list
git stash pop        # 가장 최근 항목 적용 후 삭제
```

---

## 6) 변경 되돌리기·스테이징 관리

### 🔹 Undo (워킹 디렉터리 변경 취소)

```bash
git restore {filename}
git restore .        # 전체 취소
```

### 🔹 Unstaging (스테이지 → 워킹 디렉터리로 내리기)

```bash
git restore --staged {filename}
```

---

## 7) 커밋 메시지 수정

### 🔹 직전 커밋 메시지 수정

```bash
git commit --amend
```

### 🔹 **이전 commit message 수정하기**

* (참고) 상호작용 리베이스:

  ```bash
  git rebase -i HEAD~N    # 수정할 커밋 범위
  # 해당 커밋을 'reword'로 변경 후 메시지 수정
  ```

---

## 8) Reset vs Revert

### 🔹 Reset commit — “없었던 일로 만들기”

* **강력하고 위험**: 이력 재작성. *키워드 왠만하면 사용하지 않기.*

  ```bash
  git reset --hard <commit>
  ```

### 🔹 Revert commit — “잘못을 인정하고 특정시점으로 되돌리기”

* 기존 이력 보존, **새로운 역커밋** 생성

  ```bash
  git revert --no-commit HEAD~1
  git commit
  ```
* **merge commit 되돌릴 때 -m**

  ```bash
  git revert -m 1 <merge-commit-hash> --no-edit   # commit을 따로 하지 않을 땐 '--no-edit'
  ```

---

## 9) 마일스톤 / 팀장 할 일

* **organzition 생성** *(Organization)*
* **레포 만들기**
* **이슈 템플릿 만들기** → `Settings → Issues → Set up templates`

### 이슈 템플릿 예시

```md
## Description
이슈 한줄 설명 부탁드립니다.

## tasks
- [ ] item1

## references
- [link]()
```

* **라벨**: `enhansment` *(원문 키워드 유지; 보통 'enhancement')*
* **.gitignore 셋팅**
* **프로젝트 때 사용할 베이스 파일 만들기** (공통 파일 세팅)
* 각자가 필요한 파일은 **각자** 추가

---

## 10) 내 포크로 푸시 & 이슈 연결

### 🔹 내 포크를 뜬 저장소로 푸시 (내 컴퓨터에서)

```bash
git push origin -u fizzbuzz   # branches 에 branch가 없을 경우 -u 사용
```

### 🔹 이슈 자동 연결(닫기) 키워드

* 본문/커밋/PR에서:

  * `close`, `closes`, `closed`
  * `fix`, `fixes`, `fixed`
  * `resolve`, `resolves`, `resolved`
* 예: `resolve #1`  *(이슈 연결하기)*

---

## 11) 최신 사항 받아오기 (upstream)

```bash
git remote add upstream <주소>   # git remote add upstream 주소
git remote -v                   # 확인
git fetch upstream main
git merge FETCH_HEAD            # 팀원이 업데이트 했을 때 업데이트 (원문: fetch_head)
# 또는
git pull --rebase upstream main
```

---

## 12) Pull Request 운영

* **Pull request 가 중요하다**
* 코드 리뷰/최종 컨펌/CI 연동의 중심

---

## 13) 추가적인 요청사항이 왔을 때

* PR에 **리뷰 반영 커밋** 추가 → CI 그린 확인 → 재검토 요청

---

### ✅ 요약 체크리스트

* 지금 필요 없으면 **merge**, 지금 필요하면 **rebase**
* rebase 시 충돌 해결 → `git add .` → `git rebase --continue`
* 깃허브에서 파일 수정했으면 **pull --rebase** 후 push
* 워킹 변경 취소 `git restore`, 스테이징 취소 `git restore --staged`
* **reset** 신중, 되도록 **revert** 사용
* 이슈 템플릿/라벨/PR 규칙(Conventional Commits) 정립
* 포크는 `-u`로 최초 업스트림 설정, 이슈는 `resolve #번호`로 연결
* upstream 주기적 동기화: `fetch` + `merge`(또는 `pull --rebase`)
