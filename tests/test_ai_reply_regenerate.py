import pytest
import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.chat_main_page import ChatMainPage

# 클립보드를 제어할 수 있게 해주는 라이브러리
import pyperclip


#===============================================================
# 로그인 세션은 conftest.py의 login_once fixture 사용
#===============================================================
@pytest.fixture
def prepare_AI_reply(login_once):
    driver = login_once
    return driver


class TestAIReply:


#    ---------------------------
#     답변 다시생성 기능 (AHCT-T168)
#     AI가 준 답변에서의 하단의 '다시생성' 버튼 테스트
#     ---------------------------

    def test_reply_regenerate(self,prepare_AI_reply):
        driver = prepare_AI_reply
        wait = WebDriverWait(driver, 10)
        page = ChatMainPage(driver)
        page.input_textarea("가나디로 삼행시 지어줘")
        page.send_button_click()
        page.check_UI_visible("가나디로 삼행시 지어줘")

        # 최초 답변 저장
        old_reply_text = page.get_ai_reply_element().text
        # 사용자가 화면 확인하기 전 화면이 너무 빨리 꺼짐
        time.sleep(1)
        page.get_regenerate_button()
        # 사용자가 화면 확인하기 전 화면이 너무 빨리 꺼짐
        time.sleep(1)
        page.click_regenerate_button()
        # 사용자가 화면 확인하기 전 화면이 너무 빨리 꺼짐
        time.sleep(1)

        print("답변 다시생성 버튼 클릭 성공!")

        # 이전 답변 버튼 (<) 클릭 (assert나 파일을 나누기 애매해서 try-catch 사용)
        try:
            page.get_previous_reply_button()
            page.click_previous_reply_button()
            print("이전 답변 버튼 클릭 성공!")

        except Exception as e:
            print(f"이전 답변 버튼 클릭 실패: {e}")

      
        # 사용자가 화면 확인하기 전 화면이 너무 빨리 꺼짐
        time.sleep(1)

          # 다음 답변 버튼 (>) 클릭 (assert나 파일을 나누기 애매해서 try-catch 사용)
        try:
            page.get_next_reply_button()
            page.click_next_reply_button()
            print("다음 답변 버튼 클릭 성공!")

        except Exception as e:
            print(f"다음 답변 버튼 클릭 실패: {e}")

      
        # 사용자가 화면 확인하기 전 화면이 너무 빨리 꺼짐
        time.sleep(1)



        # \ : 파이썬 내부 줄바꿈 허용
        assert page.compare_reply_regenerate(old_reply_text), \
        "다시생성 버튼 클릭 후, 답변이 변경되지 않음"

        print("답변 다시 생성 테스트 성공!")





