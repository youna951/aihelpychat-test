import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.utils import login
from utils.constants import LOGIN_ID, LOGIN_PW   # 🔥 상수 import

#브라우저 실행

def start_driver():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("--start-maximized")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(5)
    return driver

# #로그인
driver = start_driver()
login(driver, LOGIN_ID, LOGIN_PW, check_success=True)
print("로그인 완료")

#AHCT-T85 심층조사 페이지 정상이동
def test_godeepdive(driver):
    login(driver, LOGIN_ID, LOGIN_PW, check_success=True)
    
    driver.find_element(By.XPATH,"//span[contains(text(),'도구')]").click()
    print("도구 페이지 이동 완료")
    driver.find_element(By.XPATH,"//*[contains(text(),'심층 조사')]").click()
    time.sleep(1)
    print("심층 조사 페이지 이동 완료")
    count +=1
    
    title = driver.find_element(By.XPATH,"//*[@name='topic']")
    title.send_keys("강아지")
    if title.get_attribute("value") == "강아지":
        print(f"주제 : {title.get_attribute('value')} ")
    else:
        print("주제가 입력되지 않았습니다.")
        
    details = "강아지 종에대해 자세히 알려줘"
    instruction = driver.find_element(By.NAME,"instructions")
    instruction.send_keys(details)
    if instruction.get_attribute("value") == details:
        print(f"지시사항 : {instruction.get_attribute('value')}")
    else:
        print("지시사항이 입력되지 않았습니다.")
        
    assert count ==3
    

    