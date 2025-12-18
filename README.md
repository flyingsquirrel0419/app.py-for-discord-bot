## 1. 프로젝트 개요

### 주요 기능
- `.env` 파일을 통한 봇 토큰 관리
- `cogs` 폴더 내 Cog 자동 로드
- 슬래시 명령어(`/`) 자동 동기화
- 소유자 전용 Cog 리로드 명령어 제공
- 일반 명령어(`!`) + 슬래시 명령어 혼합 구조

---

## 2. 디렉터리 구조

```

project_root/
├─ bot.py              # 메인 실행 파일
├─ .env                # 환경 변수 파일
├─ cogs/
│   ├─ attendance.py   # 예시 Cog
│   └─ 기타 Cog 파일
└─ README.md

````

---

## 3. 실행 환경

### 필수 조건
- Python 3.9 이상
- discord.py 2.x

### 라이브러리 설치
```bash
pip install -U discord.py python-dotenv
````

---

## 4. 환경 변수 설정

프로젝트 루트에 `.env` 파일을 생성합니다.

```env
DISCORD_TOKEN=여기에_디스코드_봇_토큰
```

* 토큰이 없을 경우 프로그램은 즉시 오류를 발생시키고 종료됩니다.

---

## 5. 코드 구조 설명

### 5.1 Bot 클래스

* `commands.Bot` 상속
* `setup_hook()` 사용

  * Cog 자동 로딩
  * 슬래시 명령어 전체 동기화

### 5.2 Intents 설정

```python
intents = discord.Intents.default()
intents.message_content = True
```

* 접두사 명령어(`!`) 사용을 위해 필수
* Discord Developer Portal에서 **Message Content Intent** 활성화 필요

### 5.3 Cog 자동 로딩 방식

* `./cogs` 폴더가 없으면 경고 출력 후 스킵
* 모든 `.py` 파일을 `cogs.<파일명>` 형태로 자동 로드
* 로드 실패 시 에러 메시지 출력, 봇은 계속 실행

---

## 6. Cog 리로드 명령어

### 명령어

```
!sys_reload <cog_name>
```

### 사용 예시

```
!sys_reload attendance
```

### 동작 설명

* 지정한 Cog만 런타임 중 재로드
* 슬래시 명령어 재동기화 자동 수행
* 봇 소유자만 사용 가능

---

## 7. 실행 방법

```bash
python app.py
```

실행 시 콘솔 출력 예:

```
[LOAD] cogs.attendance
[SYNC] 슬래시 명령어 N개 동기화 완료
```

---

## 8. 주의 사항

* `cogs` 폴더에는 `__init__.py` 파일이 존재해야 함
* 슬래시 명령어는 Discord 서버에 반영되기까지 최대 1분 정도 소요될 수 있음
* 글로벌 슬래시 명령어는 서버가 많을 경우 적용에 시간이 더 걸릴 수 있음

