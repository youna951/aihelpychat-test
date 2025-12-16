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

from utils.common import login, logout
from utils.constants import LOGIN_ID, LOGIN_PW

PROMPT = "test_userSetting"


#==================================
# 시작 대화용 텍스트 생성:
# 예) n=1 -> 'test_userSetting_1'
#==================================
def make_startscr(n: int) -> str:
    return f"{PROMPT}_{n}"

# ------------------------------------------
# AHCT - T18 직접 설정하여 커스텀 에이전트 생성
# ------------------------------------------

# ------------------------------------------
# 토글 메뉴 내에 "에이전트 탐색" 클릭
# 에이전트 탐색 → 만들기 → 대화로 만들기까지 이동
# ------------------------------------------
def go_to_agent_builder_by_talk(driver, wait):
    # 에이전트 탐색 클릭
    agent_search = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, '//span[normalize-space(text())="에이전트 탐색"]/ancestor::li')
        )
    )
    agent_search.click()

    # 에이전트 탐색 > "+ 만들기" 클릭
    create_agent_AI = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'a[href="/ai-helpy-chat/agents/builder"]')
        )
    )
    create_agent_AI.click()

    # "설정" 탭 클릭
    create_agent_setting = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, '//button[contains(text(), "설정")]')
        )
    )
    create_agent_setting.click()


# ------------------------------------------
# 이름 입력란에 test data 입력
# ------------------------------------------
def send_prompt_for_agent_name(driver, wait, prompt: str):
    name_input = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'input[name="name"]')
        )
    )
    name_input.clear()
    name_input.send_keys(prompt)

# ------------------------------------------
# 한줄 소개란에 test data 입력
# ------------------------------------------
def send_prompt_for_agent_description(driver, wait, prompt: str):
    description_input = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'input[name="description"]')
        )
    )
    description_input.clear()
    description_input.send_keys(prompt)


# ------------------------------------------
# 규칙 입력란에 test data 입력
# ------------------------------------------
def send_prompt_for_agent_rule(driver, wait, prompt: str):
    rule_input = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'textarea[name="systemPrompt"]')
        )
    )
    rule_input.clear()
    rule_input.send_keys(prompt)


# ------------------------------------------
# 시작 대화 1~4에 test data 입력 (PROMPT + 번호)
# ------------------------------------------
def send_prompt_for_agent_startscr1(driver, wait):
    value = make_startscr(1)
    startscr1_input = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'input[name="conversationStarters.0.value"]')
        )
    )
    startscr1_input.clear()
    startscr1_input.send_keys(value)


def send_prompt_for_agent_startscr2(driver, wait):
    value = make_startscr(2)
    startscr2_input = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'input[name="conversationStarters.1.value"]')
        )
    )
    startscr2_input.clear()
    startscr2_input.send_keys(value)


def send_prompt_for_agent_startscr3(driver, wait):
    value = make_startscr(3)
    startscr3_input = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'input[name="conversationStarters.2.value"]')
        )
    )
    startscr3_input.clear()
    startscr3_input.send_keys(value)


def send_prompt_for_agent_startscr4(driver, wait):
    value = make_startscr(4)
    startscr4_input = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'input[name="conversationStarters.3.value"]')
        )
    )
    startscr4_input.clear()
    startscr4_input.send_keys(value)


# ------------------------------------------
# 미리보기 새로 고침
# ------------------------------------------
def click_refresh_preview(driver, wait):
    click_refresh = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'button[aria-label="새로고침"]')
        )
    )
    click_refresh.click()


# ------------------------------------------
# AI가 자동으로 채운 test data 검증
# ------------------------------------------

# 이름란에 PROMPT가 들어가있는지 확인
def assert_name_field(driver, wait):
    name_input = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'h6.MuiTypography-root.MuiTypography-h6.css-on088v')
        )
    )
    text_value = name_input.text.strip()
    assert PROMPT in text_value, (
        f"이름란에서 기대값 '{PROMPT}'을 찾지 못함: 실제값={text_value}"
    )


# 한줄 소개에 PROMPT가 들어가있는지 확인
def assert_description_field(driver, wait):
    description = wait.until(
        EC.visibility_of_element_located(
            (
                By.CSS_SELECTOR,
                "p.MuiTypography-root.MuiTypography-body1.css-1kktwy9",
            )
        )
    )
    desc_value = description.text.strip()
    assert PROMPT in desc_value, (
        f'한줄 소개에서 기대값 "{PROMPT}"을 찾지 못함: 실제값={desc_value}'
    )


# 규칙 입력란 value에 PROMPT가 들어가있는지 확인
def assert_rules_field(driver, wait):
    rules = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'textarea[name="systemPrompt"]')
        )
    )
    rules_value = rules.get_attribute("value")
    assert PROMPT in rules_value, (
        f'규칙 입력란에 "{PROMPT}" 없음: 실제값={rules_value}'
    )


# ------------------------------------------
# 미리보기 시작 대화 1~4에 'test_userSetting_1~4'가 들어가있는지 확인
# ------------------------------------------
def assert_preview_startscr(driver, wait, n: int):
    expected = make_startscr(n)
    item = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, f'//button//span[contains(text(), "{expected}")]')
        )
    )
    text_value = item.text.strip()
    assert expected in text_value, (
        f"시작 대화 {n}번에서 '{expected}' 없음: 실제값={text_value}"
    )


# ------------------------------------------
# 메인 테스트
# ------------------------------------------
def test_create_agent_userSetting(driver):
    # 공통 wait
    wait = WebDriverWait(driver, 10)

    # 1) 로그인
    login(driver, LOGIN_ID, LOGIN_PW, check_success=True)
    print("로그인 완료")

    # 2) 에이전트 대화로 만들기 페이지까지 이동
    go_to_agent_builder_by_talk(driver, wait)
    print("에이전트 대화로 만들기 페이지까지 이동 완료")

    # 3) 프롬프트 전송
    send_prompt_for_agent_name(driver, wait, PROMPT)
    print("이름 프롬포트 입력 완료")

    send_prompt_for_agent_description(driver, wait, PROMPT)
    print("한줄 소개 프롬포트 입력 완료")

    send_prompt_for_agent_rule(driver, wait, PROMPT)
    print("규칙 프롬포트 입력 완료")

    send_prompt_for_agent_startscr1(driver, wait)
    print("시작 대화 1 프롬포트 입력 완료")

    send_prompt_for_agent_startscr2(driver, wait)
    print("시작 대화 2 프롬포트 입력 완료")

    send_prompt_for_agent_startscr3(driver, wait)
    print("시작 대화 3 프롬포트 입력 완료")

    send_prompt_for_agent_startscr4(driver, wait)
    print("시작 대화 4 프롬포트 입력 완료")

    # 3-1) 미리보기 새로고침 (필요 시)
    click_refresh_preview(driver, wait)
    print("미리보기 새로고침 완료")

    # 4) 필드 검증
    assert_name_field(driver, wait)
    print("이름 확인 완료")

    assert_description_field(driver, wait)
    print("한줄 소개 확인 완료")

    assert_rules_field(driver, wait)
    print("규칙 확인 완료")

    assert_preview_startscr(driver, wait, 1)
    print("시작 대화 1 미리보기 확인 완료")

    assert_preview_startscr(driver, wait, 2)
    print("시작 대화 2 미리보기 확인 완료")

    assert_preview_startscr(driver, wait, 3)
    print("시작 대화 3 미리보기 확인 완료")

    assert_preview_startscr(driver, wait, 4)
    print("시작 대화 4 미리보기 확인 완료")

    # 5) 로그아웃 (정리)
    logout(driver)
    print("로그아웃 완료")

    # 
