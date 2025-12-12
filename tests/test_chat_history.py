# tests/test_chat_history_page.py
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

from pages.chat_history_page import ChatHistoryPage

#===============================================================
# 로그인 세션은 conftest.py의 login_once fixture 사용
#===============================================================
@pytest.fixture
def prepare_chat_history(login_once):
    driver = login_once
    #wait = WebDriverWait(driver, 10)
    #time.sleep(1)

    # # "검색" 아이콘 클릭
    # search_button = wait.until(
    #     EC.element_to_be_clickable(
    #         (By.XPATH, '//span[text()="검색"]')
    #     )
    # )
    # search_button.click()
    
    # try:
    #     # 특정 요소가 나타날 때까지 기다림
    #     search_modal = wait.until(
    #         EC.presence_of_element_located((By.CSS_SELECTOR, "div.MuiStack-root.css-j7qwjs"))
    #     )
    #     # ESC 키 전송
    #     ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    # except TimeoutException:
    #     # 요소가 나타나지 않으면 무시
    #     history_scroll = wait.until(
    #         EC.invisibility_of_element_located((By.XPATH, '//ul[@data-testid="virtuoso-item-list"]'))
    #     )
    return driver

#===============================================================
# [채팅 히스토리] 채팅 히스토리 스크롤 확인 (AHCT-T150)
#===============================================================
def test_check_history_visible(prepare_chat_history):
    driver = prepare_chat_history
    page = ChatHistoryPage(driver)
    assert page.check_history_visible()

#===============================================================
# [채팅 히스토리] 히스토리 타이틀 수정 - 취소 (AHCT-T153)
#===============================================================
def test_rename_history_cancel(prepare_chat_history):
    driver = prepare_chat_history
    page = ChatHistoryPage(driver)
    assert page.rename_history_cancel()

#===============================================================
# [채팅 히스토리] 히스토리 타이틀 삭제 - 취소 (AHCT-T154)
#===============================================================
def test_delete_history_cancel(prepare_chat_history):
    driver = prepare_chat_history
    page = ChatHistoryPage(driver)
    assert page.delete_history_cancel()

#===============================================================
# [채팅 히스토리] 히스토리 타이틀 수정 - 정상 (AHCT-T151)
#===============================================================
def test_rename_history(prepare_chat_history):
    driver= prepare_chat_history
    page = ChatHistoryPage(driver)
    assert page.rename_history()


#===============================================================
# [채팅 히스토리] 히스토리 타이틀 삭제 - 정상 (AHCT-T152)
#===============================================================
def test_delete_history(prepare_chat_history):
    driver = prepare_chat_history
    page = ChatHistoryPage(driver)
    assert page.delete_history()
