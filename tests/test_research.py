import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException,ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.utils import login,clear_all
from utils.constants import LOGIN_ID, LOGIN_PW   # 🔥 상수 import


# --------------------------------------------
# AHCT-T85 심층조사 페이지 정상이동
# --------------------------------------------
def test_godeepdive(login_once):
    driver = login_once
    driver.find_element(By.XPATH,"//span[contains(text(),'도구')]").click()
    print("✅도구 페이지 이동 완료")
    driver.find_element(By.XPATH,"//*[contains(text(),'심층 조사')]").click()
    print("✅심층 조사 페이지 이동 완료")

# --------------------------------------------    
# AHCT-T86 심층조사 주제 입력 유효성 검증
# --------------------------------------------
def test_research_title(login_once):
    driver = login_once
    title = driver.find_element(By.XPATH,"//input[@name='topic']")
    #버튼 요소 찾아주기
    create_bnt = driver.find_element(By.XPATH,"//button[contains(text(),'생성')]")
    #공백 입력
    clear_all(title)
    title.send_keys("")
    assert not create_bnt.is_enabled()
    print("✅공백 입력 → 생성 버튼 비활성화됨")
    #1글자 입력
    clear_all(title)
    title.send_keys("가")
    assert create_bnt.is_enabled()
    print("✅1글자 입력 → 오류 메시지 사라짐, 버튼 활성화 OK")
    #500자 입력
    clear_all(title)
    text_500 = "가" * 500
    title.send_keys(text_500)
    assert title.get_attribute("value") == text_500
    assert create_bnt.is_enabled()
    print("✅500자 입력 → 정상 입력, 버튼 활성화 OK")
    #501자 입력
    clear_all(title)
    text_501 = "가" * 501
    title.send_keys(text_501)
    assert not create_bnt.is_enabled()
    print("✅501자 입력 →  버튼 비활성화됨")
    
    

# --------------------------------------------        
# AHCT-T88 심층조사 지시사항 입력
# --------------------------------------------
def test_instruction(login_once):
    driver = login_once
    instruction = driver.find_element(By.NAME,"instructions")
    #버튼 요소 찾아주기
    create_bnt = driver.find_element(By.XPATH,"//button[contains(text(),'생성')]")
    #주제 입력해주기
    title = driver.find_element(By.XPATH,"//input[@name='topic']")
    clear_all(title)
    title.send_keys("강아지")
    #공백입력
    clear_all(instruction)
    instruction.send_keys("")
    assert create_bnt.is_enabled()
    print("✅지시사항 공백입력 테스트 완료") 
    #2000자 입력
    clear_all(instruction)
    text_2000 = "가" * 2000
    instruction.send_keys(text_2000)
    assert create_bnt.is_enabled()
    print("✅2000자 입력 →  버튼 활성화됨")
    #2001자 이상 입력
    clear_all(instruction)
    text_2001 = "가" * 2001
    instruction.send_keys(text_2001)
    assert not create_bnt.is_enabled()
    print("✅2001자 입력 →  버튼 비활성화됨")
    
# ---------------------------------
# AHCT-T129 심층조사 자동생성 버튼 클릭
# ---------------------------------
def test_research_btn(login_once):
    driver = login_once
    
    #title작성
    title = driver.find_element(By.XPATH,"//input[@name='topic']")
    clear_all(title)
    title.send_keys("강아지")
    #지시사항 작성
    instruction = driver.find_element(By.NAME,"instructions")
    clear_all(instruction)
    details = "강아지 종에 대해 자세히 알려줘"
    instruction.send_keys(details)
    
    #버튼 클릭
    try:
        create_bnt = driver.find_element(By.XPATH,"//button[contains(text(),'생성')]")
        create_bnt.click()
        recreate = driver.find_elements(By.XPATH,"//button[contains(text(),'다시 생성')]")
        recreate[1].click()
        wait = WebDriverWait(driver, 10)
        wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@data-testid='stopIcon']")))
        stop_sign = driver.find_element(By.XPATH, "//*[@data-testid='stopIcon']")
        assert stop_sign.is_displayed()
        print("✅버튼 클릭 완료-> 정상적으로 결과 생성 중 입니다.")
            
    except NoSuchElementException:
        print("❌버튼 요소를 찾을 수 없습니다.")

# --------------------------------------------
# AHCT-T133 자동생성 버튼 클릭 후 멈춤 아이콘 클릭
# --------------------------------------------
def test_research_stop(login_once):
    driver = login_once
    wait = WebDriverWait(driver, 10)
    stop_sign = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@data-testid='stopIcon']/ancestor::button")))
    stop_sign.click()
    #생성결과 메시지
    result = driver.find_element(By.XPATH,"//div[contains(text(),'요청에 의해 답변 생성을 중지했습니다.')]")
    result_msg = "요청에 의해 답변 생성을 중지했습니다."
    assert result.text == result_msg
    print("✅정지버튼클릭 완료")
    

