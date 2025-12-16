import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# 운영체제 별 나눌 때 씀
import sys
# 키보드 입력 받음
from selenium.webdriver.common.keys import Keys


class ChatMainPage:
    def __init__(self, logged_in_driver):
        driver = logged_in_driver
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)


    # ==========================
    # 공통 요소/행동
    # ==========================

    # 텍스트 입력
    def input_textarea(self, text: str = ""):
        textarea = self.wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, 'textarea[placeholder="메시지를 입력해 주세요."]')
            )
        )
        textarea.send_keys(text)
        return textarea

    # 보내기 버튼 클릭
    def send_button_click(self):
        send_button = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@type='button' and @aria-label='보내기']")
            )
        )
        send_button.click()
        return send_button

    # 전송된 메시지가 UI에 나타나는지 확인
    def check_response(self, text: str = ""):
        response = self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    (
                        f"//span[@data-status='complete' and text()='{text}']"
                        if text
                        else "//span[@data-status='complete']"
                    ),
                )
            )
        )
        return response

    # 답장이 왔는지만 확인 (내용 무시)
    def input_and_check_response(self, text: str = ""):
        self.input_textarea(text)
        self.send_button_click()
        return self.check_response(text)
    
      # 답변 하단 '복사'버튼 찾기  
    def get_copy_button(self):
        return self.wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'button[aria-label="복사"]')
            )
        )
    # 답변 하단 '복사'버튼 클릭
    def click_copy_button(self):
        self.get_copy_button().click()

     # 전체 답변 내용 요소 접근
    def get_ai_reply_element(self):
        return self.wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "div.elice-aichat__markdown")
            )
        )

    
    # 붙여넣기 (os별로 단축키 다름)
    def paste_clipboard(self, textarea):
        textarea.click()
        if sys.platform == "darwin":
            textarea.send_keys(Keys.COMMAND, 'v')
        else:
            textarea.send_keys(Keys.CONTROL, 'v')




