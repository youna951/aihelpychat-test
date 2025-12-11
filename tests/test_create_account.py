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
  
# 회원가입 > 잘못된 이메일 형식 입력 테스트(AHCT-T123)
'''
def test_create_account_wrong_email(driver):
    wrong_email = "abcdefg@com"
    driver.get("https://qaproject.elice.io/ai-helpy-chat")
    time.sleep(1)
    
    driver.find_element(
        By.XPATH, '//a[contains(text(), "Create account")]'
    ).click()
    time.sleep(1)
    
    driver.find_element(
        By.XPATH, '//button[contains(text(), "Create account with email")]'
    ).click()
    time.sleep(1)
    
    driver.find_element(
        By.XPATH, '//input[@name="loginId"]'
    ).send_keys(wrong_email)
    time.sleep(1)
    
    try:
        error_msg = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//p[contains(text(), "Email address is incorrect.")]')
                #(By.ID, ":r3:-helper-text")
            )
        )
        #assert error_msg.is_displayed(), "잘못된 이메일 입력 시 오류 메시지가 표시되지 않음"
        assert "Email address is incorrect." in error_msg.text, f"예상 오류 메시지와 다름. 실제 메시지: '{error_msg.text}'"
    except:
        assert False, "이메일 입력시 예상된 오류 메시지를 찾지 못함"

    print("잘못된 이메일 입력 테스트 완료!")
'''    
    
# 회원가입 > 짧거나 형식에 맞지 않는 비밀번호 입력 테스트(AHCT-T123)
'''
def test_create_account_wrong_password(driver):
    wrong_email = "abcdefg@com"
    wrong_password = "abcdefg"
    driver.get("https://qaproject.elice.io/ai-helpy-chat")
    time.sleep(1)
    
    driver.find_element(
        By.XPATH, '//a[contains(text(), "Create account")]'
    ).click()
    time.sleep(1)
    
    driver.find_element(
        By.XPATH, '//button[contains(text(), "Create account with email")]'
    ).click()
    time.sleep(1)
    
    driver.find_element(
        By.XPATH, '//input[@name="loginId"]'
    ).send_keys(wrong_email)
    time.sleep(1)
    
    driver.find_element(
        By.XPATH, '//input[@name="password"]'
    ).send_keys(wrong_password)
    time.sleep(1)
    
    try:
        error_msg = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//p[contains(text(), "Please make your password stronger! Try to combine at least 8 characters including English, numeric and special characters.")]')
                #(By.ID, ":r3:-helper-text")
            )
        )        
        assert "Please make your password stronger! Try to combine at least 8 characters including English, numeric and special characters." in error_msg.text, f"예상 오류 메시지와 다름. 실제 메시지: '{error_msg.text}'"
    except:
        assert False, "비밀번호 입력시 예상된 오류 메시지를 찾지 못함"

    print("잘못된 비밀번호 입력 테스트 완료!")
'''    
    
@pytest.mark.parametrize(
    "email, password, email_error, pw_error",
    [
        # 이메일 오류만 발생하는 경우
        ("abcdefg@com", "ValidPass123!", "Email address is incorrect.", None),

        # 비밀번호 오류만 발생하는 경우
        ("validmail@test.com", "abcdefg",
         None,
         "Please make your password stronger! Try to combine at least 8 characters including English, numeric and special characters."),
    ]
)
#회원가입 > 잘못된 이메일 / 짧거나 형식에 맞지 않는 비밀번호 입력 테스트(AHCT-T123)
def test_create_account_input_validation(driver, email, password, email_error, pw_error):
    #driver = driver_session
    driver.get("https://qaproject.elice.io/ai-helpy-chat")
    time.sleep(1)

    driver.find_element(By.XPATH, '//a[contains(text(), "Create account")]').click()
    time.sleep(1)

    driver.find_element(By.XPATH, '//button[contains(text(), "Create account with email")]').click()
    time.sleep(1)

    # 1) 이메일 입력
    driver.find_element(By.XPATH, '//input[@name="loginId"]').send_keys(email)
    time.sleep(0.5)

    # 이메일 오류 메시지가 기대될 경우만 검증
    if email_error:
        try:
            email_err_el = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located(
                    (By.XPATH, f'//p[contains(text(), "{email_error}")]')
                )
            )
            assert email_error in email_err_el.text
            print("이메일 오류 메시지 확인됨 ✔️")
        except:
            assert False, f"예상 이메일 오류 메시지 못 찾음: {email_error}"

    # 2) 비밀번호 입력
    driver.find_element(By.XPATH, '//input[@name="password"]').send_keys(password)
    time.sleep(0.5)

    # 비밀번호 오류 메시지가 기대될 경우만 검증
    if pw_error:
        try:
            pw_err_el = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located(
                    (By.XPATH, f'//p[contains(text(), "{pw_error}")]')
                )
            )
            assert pw_error in pw_err_el.text
            print("비밀번호 오류 메시지 확인됨 ✔️")
        except:
            assert False, f"예상 비밀번호 오류 메시지 못 찾음: {pw_error}"

    print("입력 검증 테스트 완료!")
    
    
#AHCT-T144 (1.0) [로그인] Forgot your password? > 이메일 인증 / Go to login page > Remove history
