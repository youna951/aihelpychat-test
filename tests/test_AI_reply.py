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

    # ---------------------------
    # 답변 복사 기능 (AHCT-T119)
    # AI가 준 답변에서의 하단의 '복사' 버튼 테스트
    # ---------------------------

    def test_reply_copy(self,prepare_AI_reply):
        driver = prepare_AI_reply
        wait = WebDriverWait(driver, 10)
        page = ChatMainPage(driver)
        page.input_textarea("사과의 색깔은?")
        page.send_button_click()
        page.check_response("사과의 색깔은?")


        copy_button = page.wait.until(
        EC.element_to_be_clickable(
        (By.CSS_SELECTOR, 'button[aria-label="복사"]')
    )
)
        copy_button.click()
        print("답변 복사버튼 클릭 완료!")

        ai_reply = driver.find_element(By.CSS_SELECTOR, "div.elice-aichat__markdown").text
        # 라이브러리 통해서 답변 내용 복사 
        pyperclip.copy(ai_reply)

        # 요소 다시 접근
        textarea = page.wait.until(
        EC.presence_of_element_located(
        (By.CSS_SELECTOR, 'textarea[placeholder="메시지를 입력해 주세요."]')
    )
)
        # 붙여넣기는 chat_main_page에 만든 메서드 사용
        page.paste_clipboard(textarea)
        time.sleep(0.5)

        pasted_text = textarea.get_attribute("value")

        assert pasted_text == ai_reply
        print("답변 복사 기능 테스트 완료!")


    
        





    



