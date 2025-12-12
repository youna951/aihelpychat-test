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

# ------------------------------------------
# AHCT-T164 에이전트 탐색 페이지 이동
# ------------------------------------------   
    # ------------------------------------------
    #토글 메뉴 내에 "에이전트 탐색" 클릭
    # ------------------------------------------
def go_to_agent_search(driver, wait):
    agent_search = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, '//span[normalize-space(text())="에이전트 탐색"]/ancestor::li')
        )
    )
    agent_search.click()

    # 2) 페이지 로딩 대기 - 타이틀/고유 요소 등장 확인
    wait.until(
        EC.presence_of_element_located(
            (By.XPATH, '//a[contains(text(), "내 에이전트")]')
        )
    )

# ------------------------------------------
# 메인 테스트
# ------------------------------------------
def test_go_to_agent_search(driver):
    wait = WebDriverWait(driver, 10)
    # 1) 로그인
    login(driver, LOGIN_ID, LOGIN_PW)
    print("로그인 성공")
    # 2) 이동
    go_to_agent_search(driver, wait)
    print("에이전트 탐색 페이지 이동")
    # 3) URL 검증
    current_url = driver.current_url
    assert "ai-helpy-chat/agents" in current_url, f"URL 잘못됨: {current_url}"
    print("URL 체크 완료")
    # 4) 고유 요소 존재 검증
    page_title = driver.find_element(By.XPATH, '//a[contains(text(), "내 에이전트")]')
    assert page_title is not None, "페이지 타이틀이 보이지 않음"
    print("UI 요소 확인 완료")

    # 5) 로그아웃
    logout(driver)
    print("로그아웃 완료")

