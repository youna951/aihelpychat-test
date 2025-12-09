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

from utils.utils import login, logout
from utils.constants import LOGIN_ID, LOGIN_PW   # 🔥 상수 import

@pytest.fixture
def driver():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("--start-maximized")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(5)

    yield driver
    driver.quit()

#정상 로그인/로그아웃 테스트
def test_login_logout(driver):
    # 🔥 상수 사용
    login(driver, LOGIN_ID, LOGIN_PW, check_success=True)
    logout(driver)
    print("로그인 및 로그아웃 테스트 완료!")

    
#비정상 로그인(잘못된 이메일 형식)
def test_login_invalid_email(driver):
    # 잘못된 이메일과 정상 비밀번호
    invalid_email = "invalid_id"  # 이메일 형식 아님
    password = ""

    # 로그인 시도
    login(driver, invalid_email, password, check_success=False)

    try:
        error_msg = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//p[contains(text(), "Invalid email format.")]')
                #(By.ID, ":r3:-helper-text")
            )
        )
        #assert error_msg.is_displayed(), "잘못된 이메일 입력 시 오류 메시지가 표시되지 않음"
        assert "Invalid email format" in error_msg.text, f"예상 오류 메시지와 다름. 실제 메시지: '{error_msg.text}'"
    except:
        assert False, "로그인 실패 시 예상된 오류 메시지를 찾지 못함"

    print("잘못된 이메일 로그인 테스트 완료!")


#비정상 로그인(짧은 비밀번호)
def test_login_short_password(driver):
    
    # 정상 이메일, 8자 이하 비밀번호
    valid_email = LOGIN_ID
    short_password = "1234567"  # 7자 (8자 이하)

    # 로그인 시도, 성공 검증은 하지 않음
    login(driver, valid_email, short_password, check_success=False)

    # 비밀번호 짧음으로 인한 로그인 실패 메시지 확인
    try:
        error_msg = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//p[contains(text(), "Please enter a password of at least 8 digits.")]')                
            )
        )
        assert "Please enter a password of at least 8 digits." in error_msg.text, f"예상 오류 메시지와 다름. 실제 메시지: '{error_msg.text}'"
    except:
        assert False, "로그인 실패 시 예상된 오류 메시지를 찾지 못함"

    print("비밀번호 8자 이하 입력 테스트 완료!")
    
    
#비정상 로그인(틀린 비밀번호)
def test_login_wrong_password(driver):
    
    # 정상 이메일, 8자 이하 비밀번호
    valid_email = LOGIN_ID
    short_password = "wrongpassword"  #잘못된 비밀번호

    # 로그인 시도, 성공 검증은 하지 않음
    login(driver, valid_email, short_password, check_success=False)

    # 비밀번호 틀림으로 인한 로그인 실패 메시지 확인
    try:
        error_msg = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//p[contains(text(), "Email or password does not match")]')                
            )
        )
        assert "Email or password does not match" in error_msg.text, f"예상 오류 메시지와 다름. 실제 메시지: '{error_msg.text}'"
    except:
        assert False, "로그인 실패 시 예상된 오류 메시지를 찾지 못함"

    print("비밀번호 8자 이하 입력 테스트 완료!")
