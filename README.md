# 🧪 Web Service QA Automation Project

본 프로젝트는 AI 기반 웹 서비스의 주요 기능에 대해  
품질 검증을 목적으로 테스트 케이스 설계 및 자동화 테스트를 수행한 QA 프로젝트입니다.  
Page Object Model(POM) 구조를 적용하여 유지보수성을 고려한 테스트 환경을 구성했으며,  
PPT 생성, 수업안 생성, 생활기록부 생성, 자료 조사 등  
사용자 시나리오 기반 기능 흐름을 중심으로 검증을 진행했습니다.

## 🙋‍♀️ 담당 역할

- 기능 명세 기반 테스트 케이스 작성 (총 95건)
- 정상/예외/경계값 테스트 설계
- pytest + Selenium 기반 자동화 테스트 구현
- 테스트 결과 정리 및 이슈 리포트 작성

  ## 📂 Project Structure (My Contribution)

```text
pages/
 ├─ base_page.py                  # 공통 Page Object 구조 설계
 ├─ ppt_page.py                   # PPT 생성 페이지
 ├─ school_life_record_page.py    # 생활기록부 생성 페이지
 └─ lessonplan_page.py            # 수업안 생성 페이지

tests/
 ├─ test_ppt.py                   # PPT 생성 테스트
 ├─ test_school_record.py         # 생활기록부 생성 테스트
 ├─ test_chat_history.py          # 채팅 히스토리 검증
 ├─ test_research.py              # 자료 조사 테스트
 └─ test_lessonplan.py            # 수업안 생성 기능 테스트

utils/
 └─ common.py                     # 공통 동작 및 헬퍼 함수

conftest.py                       # pytest fixture 및 드라이버 설정
```

## 🛠 Tech Stack

- Language: Python
- Test Framework: pytest
- Automation: Selenium
- 협업 도구: Git, GitLab
- OS: Windows,Mac
- Issue Tracking: Jira, Google Sheets

