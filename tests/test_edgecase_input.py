import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys, os

# 추가
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys


# utils 경로 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.common import login, logout
from utils.constants import LOGIN_ID, LOGIN_PW

# ---------------------------
# 답변 생성 중 취소 버튼 클릭 (AHCT-T109)
# ---------------------------


def test_cancel_reply(logged_in_driver):
    driver = logged_in_driver
    wait = WebDriverWait(driver, 15)

    # 요소 선언 (랜더링 되면 요소를 못찾아서, 필요할 때마다 꺼내쓰기)
    cancel_div_locator = (By.CSS_SELECTOR, "div.e1qzu3c80.css-bzu0e4.e166ifs70")


    # 1. 입력창 찾기
    input_box = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'textarea[placeholder="메시지를 입력해 주세요."]')
        )
    )

    # 2. 메시지 입력
    test_message = "답변 생성 중 취소 버튼 클릭"
    input_box.send_keys(test_message)

    # 3. 보내기 클릭
    send_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[@type='button' and @aria-label='보내기']")
        )
    )
    send_button.click()

    # 4. 취소 버튼이 실제로 화면에 보일 때까지 기다림
    cancel_button = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//button[@type='button' and @aria-label='취소']")
        )
    )

    
    time.sleep(4)

    # 5. 취소 버튼 클릭 
    cancel_button.click()

    # 6. 복사/다시생성 div가 나타나면 → PASS 처리
    try:
        # stale 피하기 위해 필요할 때 요소를 꺼내 씀
        wait.until(EC.visibility_of_element_located(cancel_div_locator))
        assert True  # PASS
        print("답변 생성 중 취소 버튼 클릭 테스트 성공!")
    except (TimeoutException, StaleElementReferenceException):
        assert False, "중간 취소가 실패됨."


# ---------------------------
# 답변 생성 중 텍스트 입력 (AHCT-T116)
# ---------------------------

def test_writing_reply(login_once):
    driver = login_once
    wait = WebDriverWait(driver, 15)

     # 1. 입력창 찾기
    input_box = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'textarea[placeholder="메시지를 입력해 주세요."]')
        )
    )

    # 2. 메시지 입력
    test_message = "토스트를 먹는 행복한 고양이 그려줘"
    input_box.send_keys(test_message)

    # 3. 보내기 클릭
    send_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[@type='button' and @aria-label='보내기']")
        )
    )
    send_button.click()

    time.sleep(5)
   

    # 4. 답변 생성 중 메세지 보내기
    # textarea 안정화 대기 (DOM detach/attach 순간 방지)
    wait.until(
    lambda d: d.find_element(
        By.CSS_SELECTOR,
        'textarea[placeholder="메시지를 입력해 주세요."]'
    ).is_enabled()
)

 

    # UI 바뀌어서 input_box는 stale됨 → 다시 찾아야 함
    input_box = wait.until(
    EC.presence_of_element_located((
        By.CSS_SELECTOR,
        'textarea[placeholder="메시지를 입력해 주세요."]'
    ))
)


    test_message = "답변 생성 중 메세지 보내기 (키보드 엔터입력 받음)\n""-> 답변생성중에는 메세지가 보내지지 않고 줄바꿈만 됨"
    input_box.send_keys(test_message)

    # 엔터 입력 받음
    input_box.send_keys(Keys.ENTER)

    time.sleep(8)

    # 줄바꿈이 생겼는지 확인
    value_after_enter = input_box.get_attribute("value")
    assert "\n" in value_after_enter, "엔터 입력시 줄바꿈이 되어야 한다."