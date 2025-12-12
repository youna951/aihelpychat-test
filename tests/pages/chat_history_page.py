import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utils.common import clear_all


class ChatHistoryPage:
    def __init__(self, logged_in_driver):
        driver = logged_in_driver
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # ==========================
    # 공통 요소/행동
    # ==========================
    def get_first_chat(self):
        chat_list = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'ul[data-testid="virtuoso-item-list"]'))
        )
        return chat_list.find_element(By.CSS_SELECTOR, 'a')

    def open_menu(self, chat_element):
        """첫 번째 히스토리 항목 hover → 메뉴 클릭"""
        ActionChains(self.driver).move_to_element(chat_element).perform()
        time.sleep(0.2)
        ellipsis_icon = chat_element.find_element(By.CSS_SELECTOR, 'svg[data-icon="ellipsis-vertical"]')
        ellipsis_icon.click()

    def modal_closed(self, xpath):
        try:
            WebDriverWait(self.driver, 5).until(EC.invisibility_of_element_located((By.XPATH, xpath)))
            return True
        except TimeoutException:
            return False

    # ==========================
    # [채팅 히스토리] 채팅 히스토리 스크롤 확인 (AHCT-T150)
    # ==========================
    def check_history_visible(self):
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//ul[@data-testid="virtuoso-item-list"]')))
            print("[채팅 히스토리] 채팅 히스토리 스크롤 확인 (AHCT-T150) 성공!")
            return True
        except TimeoutException:
            print("[채팅 히스토리] 채팅 히스토리 스크롤 확인 (AHCT-T150) 실패 / check_history_visible")
            return False

    # --------------------------
    # [채팅 히스토리] 히스토리 타이틀 수정 - 정상 (AHCT-T151)
    # --------------------------
    def rename_history(self, new_title="이름변경 자동화 테스트"):
        first_chat = self.get_first_chat()
        self.open_menu(first_chat)

        rename_btn = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "이름 변경")]'))
        )
        rename_btn.click()

        input_box = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'form input[type="text"]')))
        clear_all(input_box)
        input_box.send_keys(new_title)

        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "저장")]'))).click()

        try:
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="alert"]')))
            print("[채팅 히스토리] 히스토리 타이틀 수정 - 정상 (AHCT-T151) 성공!")
            return True
        except TimeoutException:
            print("[채팅 히스토리] 히스토리 타이틀 수정 - 정상 (AHCT-T151) 실패 / rename_history")
            return False

    # --------------------------
    # [채팅 히스토리] 히스토리 타이틀 수정 - 취소 (AHCT-T153)
    # --------------------------
    def rename_history_cancel(self):
        first_chat = self.get_first_chat()
        self.open_menu(first_chat)

        rename_btn = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "이름 변경")]'))
        )
        rename_btn.click()

        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "취소")]'))).click()

        if self.modal_closed('//h2[contains(text(), "이름 변경")]'):
            print("[채팅 히스토리] 히스토리 타이틀 수정 - 취소 (AHCT-T153) 성공!")
            return True
        else:
            print("[채팅 히스토리] 히스토리 타이틀 수정 - 취소 (AHCT-T153) 실패 / rename_history_cancel")
            return False

    # --------------------------
    # [채팅 히스토리] 히스토리 타이틀 삭제 - 정상 (AHCT-T152)
    # --------------------------
    def delete_history(self):
        first_chat = self.get_first_chat()
        self.open_menu(first_chat)

        delete_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//p[contains(text(), "삭제")]')))
        delete_btn.click()

        confirm_delete = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "삭제")]')))
        confirm_delete.click()

        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "대화가 삭제되었습니다!")]')))
            print("[채팅 히스토리] 히스토리 타이틀 삭제 - 정상 (AHCT-T152) 성공!")
            return True
        except TimeoutException:
            print("[채팅 히스토리] 히스토리 타이틀 삭제 - 정상 (AHCT-T152) 실패 / delete_history")
            return False

    # --------------------------
    # [채팅 히스토리] 히스토리 타이틀 삭제 - 취소 (AHCT-T154)
    # --------------------------
    def delete_history_cancel(self):
        first_chat = self.get_first_chat()
        self.open_menu(first_chat)

        delete_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//p[contains(text(), "삭제")]')))
        delete_btn.click()

        cancel_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "취소")]')))
        cancel_btn.click()

        if self.modal_closed('//h2[contains(text(), "삭제 확인")]'):
            print("[채팅 히스토리] 히스토리 타이틀 삭제 - 취소 (AHCT-T154) 성공!")
            return True
        else:
            print("[채팅 히스토리] 히스토리 타이틀 삭제 - 취소 (AHCT-T154) 실패 / delete_history_cancel")
            return False
