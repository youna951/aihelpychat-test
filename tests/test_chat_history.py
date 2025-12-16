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
    #driver = logged_in_driver
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
    
    
#===============================================================
# [채팅 히스토리] 히스토리 클릭시 전체 내용 조회 (AHCT-T155)
#===============================================================
def test_search_history_click(prepare_chat_history):
    driver = prepare_chat_history
    page = ChatHistoryPage(driver)
    assert page.search_history_click()   
 
    
#===============================================================
# [채팅 히스토리] 새 대화 버튼 클릭 - 초기화면에서 (AHCT-T156)
#===============================================================
def test_click_new_btn1(prepare_chat_history):
    driver = prepare_chat_history
    page = ChatHistoryPage(driver)
    assert page.click_new_btn1()


#===============================================================
# [채팅 히스토리] 새 대화 버튼 클릭 - 다른 히스토리 클릭 중 (AHCT-T157)
#===============================================================
def test_click_new_btn2(prepare_chat_history):
    driver = prepare_chat_history
    page = ChatHistoryPage(driver)
    assert page.click_new_btn2()


#===============================================================
# [채팅 히스토리] 히스토리 검색 - 정상 조회 (AHCT-T158)
#===============================================================
def test_search_history_function(prepare_chat_history):
    driver = prepare_chat_history
    page = ChatHistoryPage(driver)
    assert page.search_history_function()
    
    
#===============================================================
# [채팅 히스토리] 히스토리 검색 - 검색 결과 없음 (AHCT-T159)
#===============================================================
def test_search_history_function_no_result(prepare_chat_history):
    driver = prepare_chat_history
    page = ChatHistoryPage(driver)
    assert page.search_history_function_no_result()
    
    
#===============================================================
# [채팅 히스토리] 히스토리 검색 - 취소 (AHCT-T160)
#===============================================================
def test_search_history_function_cancel(prepare_chat_history):
    driver = prepare_chat_history
    page = ChatHistoryPage(driver)
    assert page.search_history_function_cancel()
    
    
# --------------------------        
# [채팅 히스토리] 메뉴 접기/펼치기 - 상단 ‘메뉴 아이콘’ 버튼 (AHCT-T161)
# --------------------------
def test_top_menu_off_on(prepare_chat_history):
    driver = prepare_chat_history
    page = ChatHistoryPage(driver)
    assert page.top_menu_off_on()


# --------------------------        
# [채팅 히스토리] 메뉴 접기/펼치기 - 하단 ‘메뉴 접기’ 버튼 (AHCT-T162)
# --------------------------
def test_bottom_menu_off_on(prepare_chat_history):
    driver = prepare_chat_history
    page = ChatHistoryPage(driver)
    assert page.bottom_menu_off_on()


# --------------------------        
# [채팅 히스토리] 메뉴 접기/펼치기 - 메뉴 자동 열림/닫힘 (AHCT-T163)
# --------------------------
def test_auto_menu_off_on(prepare_chat_history):
    driver = prepare_chat_history
    page = ChatHistoryPage(driver)
    assert page.auto_menu_off_on()
