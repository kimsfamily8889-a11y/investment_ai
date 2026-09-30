# investment-ai

AI 투자팀 시스템의 로컬 개발환경입니다. 현재 범위는 PostgreSQL과 Python 연결 검증입니다.
투자 Agent, ETF 수집, 주문 기능 및 웹 서버는 구현하지 않았습니다.

## 로컬 환경

- Python 3.12 / 프로젝트 가상환경 `.venv`
- PostgreSQL 18.6 / Windows 서비스 `postgresql-x64-18` (자동 시작)
- 서버 `127.0.0.1:5432`, 데이터베이스 `investment_ai`
- 프로젝트 계정 `investment_ai_app`: DB 소유자이며 슈퍼유저·다른 DB 생성·역할 생성 권한 없음
- 데이터베이스 인코딩 UTF-8, 기본 시간대 UTC
- psycopg 3, SQLAlchemy, python-dotenv

2026-09-28 설치 및 접속 검증 완료. pgAdmin도 설치되어 있습니다.
PostgreSQL은 localhost에서만 접속을 받으며 SCRAM 비밀번호 인증을 사용합니다.
기존 SQL Server의 `MSSQLSERVER` 서비스는 중지·수동 시작으로 전환했고 설치본은 보존했습니다.
투자 관련 영구 테이블은 아직 없습니다.

## 연결 확인

프로젝트 루트의 PowerShell에서 실행합니다. 가상환경 활성화나 전역 PATH 변경은 필요 없습니다.

```powershell
.\.venv\Scripts\python.exe scripts\check_db.py
```

연결, 임시 테이블 쓰기, 한글 문자열, 정확한 소수 금액을 검사하고 롤백합니다.
영구 테이블은 만들지 않습니다.

## 설정 및 비밀번호

`.env.example`은 공유 가능한 예시이며, 실제 비밀번호는 Git 제외 파일 `.env`에 있습니다.
`.env`는 평문 연결 설정이므로 공유하지 마세요. Windows 파일 접근 권한을 제한합니다.
관리자 `postgres`의 비밀번호는 `.local/private/postgres-admin.xml`에 Windows DPAPI로
암호화하여 보관합니다. 생성한 Windows 계정과 PC에서만 복호화할 수 있습니다.
이 파일과 `.env`는 일반 소스 백업·Git 커밋에 포함하지 않습니다.

pgAdmin에서 서버를 등록할 때 호스트 `127.0.0.1`, 포트 `5432`, 유지관리 DB `investment_ai`,
사용자 `investment_ai_app`과 `.env`의 비밀번호를 사용합니다.

## 의존성

`requirements.txt`에는 직접 의존성 범위를, `requirements.lock.txt`에는 검증한 환경의 정확한
버전을 기록합니다. 같은 Python/Windows 환경을 재구성할 때:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.lock.txt
```

새 PC에는 PostgreSQL 설치와 별도 DB/계정 생성이 필요합니다. 위 명령은 Python 패키지만 설치합니다.
`.local`의 스크립트는 이 PC에서 사용한 일회성 설치 기록이며 자동 재실행용이 아닙니다.

## 다음 단계

ETF·가격·분배금·포트폴리오 스키마를 먼저 정하고 Alembic을 도입합니다.
그 후 데이터 수집·계산 Tool, MCP 서버, Agent, FastAPI 순으로 확장합니다.
