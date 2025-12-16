
import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import sys, os

# utils 경로 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.utils import login, logout
from utils.constants import LOGIN_ID, LOGIN_PW

PROMPT = '더이상 질문하지 말고 "비서봇" 이름의 에이전트를 생성해줘'

# ------------------------------------------
# AHCT - T17 대화로 커스텀 에이전트 생성
# ------------------------------------------
    
# ------------------------------------------
#토글 메뉴 내에 "에이전트 탐색" 클릭
#에이전트 탐색 → 만들기 → 대화로 만들기까지 이동
# ------------------------------------------
def go_to_agent_builder_by_talk(driver, wait):
    agent_search = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, '//span[normalize-space(text())="에이전트 탐색"]/ancestor::li')
        )
    )
    agent_search.click()

# ------------------------------------------
# 에이전트 탐색>"+ 만들기" 클릭
# ------------------------------------------

    create_agent_AI = wait.until(
    EC.element_to_be_clickable(
        (By.CSS_SELECTOR, 'a[href="/ai-helpy-chat/agents/builder"]')
        )
    )
    create_agent_AI.click()

# ------------------------------------------
# "대화로 만들기" 클릭
# ------------------------------------------

    create_agent_talk = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, '//button[contains(text(), "대화로 만들기")]')
        )
    )
    create_agent_talk.click()

# ------------------------------------------
# 대화창에 test data 입력
#"대화창에 프롬프트 입력 후 전송
# ------------------------------------------
def send_prompt_for_agent_creation(driver, wait, prompt: str):
    chat_input = wait.until(
    EC.visibility_of_element_located(
        (By.XPATH, '//textarea[@name="input"]')
        )
    )

    chat_input.clear()
    chat_input.send_keys(prompt)

    #대화 내용 전송
    send_button = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'button[aria-label="보내기"]')  
        )
    )
    send_button.click()

# ------------------------------------------
# AI가 자동으로 채운 에이전트 필드 값 검증
# ------------------------------------------
#이름 입력란에 "비서봇"이 입력되어있으면 OK
def assert_name_field(driver, wait):
    name_input = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'input[name="name"]')
        )
    )
    WebDriverWait(driver, 30).until(
        lambda d: name_input.get_attribute("value") != ""
    )

    name_value = name_input.get_attribute("value")
    assert "비서봇" in name_value, f'에이전트 이름에 "비서봇" 없음: {name_value}'

# 한줄 소개란에 텍스트가 1자 이상이라도 입력됐으면 OK
def assert_description_field(driver, wait):
    description = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'input[name="description"]')
        )
    )
    desc_value = description.get_attribute("value")
    assert desc_value.strip() != "", "설명 자동 생성이 되지 않았음"

#규칙 입력란에 텍스트가 1자 이상이라도 입력됐으면 OK
def assert_rules_field(driver, wait):
    rules = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'textarea[name="systemPrompt"]')
        )
    )
    rules_value = rules.get_attribute("value")
    assert rules_value.strip() != "", "규칙 자동 생성이 되지 않았음"

#시작 대화 1번 입력란에 텍스트가 1자 이상이라도 입력됐으면 OK
def assert_startscr1_field(driver, wait):
    startscr1 = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'input[name="conversationStarters.0.value"]')
        )
    )
    startscr1_value = startscr1.get_attribute("value")
    assert startscr1_value.strip() != "", "시작 대화 1번에 자동 생성이 되지 않았음"

#시작 대화 2번 입력란에 텍스트가 1자 이상이라도 입력됐으면 OK
def assert_startscr2_field(driver, wait):
    startscr2 = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'input[name="conversationStarters.1.value"]')
        )
    )
    startscr2_value = startscr2.get_attribute("value")
    assert startscr2_value.strip() != "", "시작 대화 2번에 자동 생성이 되지 않았음"

#시작 대화 3번 입력란에 텍스트가 1자 이상이라도 입력됐으면 OK
def assert_startscr3_field(driver, wait):
    startscr3 = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'input[name="conversationStarters.2.value"]')
        )
    )
    startscr3_value = startscr3.get_attribute("value")
    assert startscr3_value.strip() != "", "시작 대화 3번에 자동 생성이 되지 않았음"

#시작 대화 4번 입력란에 텍스트가 1자 이상이라도 입력됐으면 OK
def assert_startscr4_field(driver, wait):
    startscr4 = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'input[name="conversationStarters.3.value"]')
        )
    )
    startscr4_value = startscr4.get_attribute("value")
    assert startscr4_value.strip() != "", "시작 대화 4번에 자동 생성이 되지 않았음"


# ------------------------------------------
# 메인 테스트
# ------------------------------------------
def test_AI_Talk(driver):
# 공통 wait
    wait = WebDriverWait(driver, 10)

# 1) 로그인
    login(driver, LOGIN_ID, LOGIN_PW, check_success=True)
    print("로그인 완료")

# 2) 에이전트 대화로 만들기 페이지까지 이동
    go_to_agent_builder_by_talk(driver, wait)
    print("에이전트 대화로 만들기 페이지까지 이동 완료")

# 3) 프롬프트 전송
    send_prompt_for_agent_creation(driver, wait, PROMPT)
    print("프롬포트 입력 완료")

# 4) AI가 채워준 필드들 검증
    assert_name_field(driver, wait)
    print("이름 확인 완료")
    assert_description_field(driver, wait)
    print("한줄 소개 확인 완료")
    assert_rules_field(driver, wait)
    print("규칙 확인 완료")
    assert_startscr1_field(driver, wait)
    print("시작 대화 1 확인 완료")
    assert_startscr2_field(driver, wait)
    print("시작 대화 2 확인 완료")
    assert_startscr3_field(driver, wait)
    print("시작 대화 3 확인 완료")
    assert_startscr4_field(driver, wait)
    print("시작 대화 4 확인 완료")

# 5) 로그아웃 (정리)
    logout(driver)
    print("로그아웃 완료")





#