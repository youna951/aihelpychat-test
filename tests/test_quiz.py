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

from utils.utils import login
from utils.constants import LOGIN_ID, LOGIN_PW   # 🔥 상수 import

# --------------------------------------------
# AHCT-T79 퀴즈생성 페이지 정상 이동
# --------------------------------------------
def test_goquiz(login_once):
    driver = login_once
    driver.find_element(By.XPATH,"//span[contains(text(),'도구')]").click()
    print("도구 페이지 이동 완료")
    driver.find_element(By.XPATH,"//*[contains(text(),'퀴즈 생성')]").click()
    time.sleep(1)
    print("퀴즈 생성 페이지 이동 완료")

# --------------------------------------------
# AHCT-T80 퀴즈생성 유형 드롭박스 표시
# --------------------------------------------
def test_quiz_type(login_once):
    driver = login_once
    wait = WebDriverWait(driver, 10)
    qz_type_dpbox = driver.find_element(By.ID,"mui-component-select-quiz_configs.0.option_type")
    qz_type_dpbox.click()
    qz_type = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//li[@role='option']")))
    type_texts = [opt.text for opt in qz_type]
    print("퀴즈 종류:",type_texts)
    qz_type[0].click()
    time.sleep(2)
    #검증
    for opt_text in type_texts:
        qz_type_dpbox.click()
        option = wait.until(EC.element_to_be_clickable((By.XPATH, f"//li[@role='option' and text()='{opt_text}']")))
        option.click()
        selected_value = qz_type_dpbox.text
        print(f"선택된 값:{selected_value}")
        assert selected_value==opt_text,f"선택값 불일치 : 기대값={opt_text}, 실제값={selected_value}"
    print("퀴즈 생성 유형 검증 완료")
    
# --------------------------------------------
# AHCT-T81 퀴즈생성 난이도 드롭박스 표시
# --------------------------------------------
def test_quiz_level(login_once):
    driver = login_once
    wait = WebDriverWait(driver, 10)