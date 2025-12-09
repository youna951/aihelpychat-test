import pytest
import time
import pyautogui
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import sys, os

# utils 경로 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.utils import login, logout
from utils.constants import LOGIN_ID, LOGIN_PW

# ---------------------------
# 브라우저 실행/종료 fixture
# ---------------------------
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

# ---------------------------
# 파일 업로드 테스트
# ---------------------------
def test_plus_fileUpload(driver):
    # 로그인
    login(driver, LOGIN_ID, LOGIN_PW, check_success=True)
    time.sleep(2)

    wait = WebDriverWait(driver, 10)

    # ---------------------------
    # 플러스 버튼 클릭 (업로드 메뉴 열기)
    # ---------------------------
    plus_button = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'button:has(svg[data-testid="plusIcon"])')
        )
    )
    plus_button.click()
    time.sleep(1)

    # ---------------------------
    # 파일 업로드 버튼 클릭
    # ---------------------------
    upload_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, '//span[text()="파일 업로드"]')
        )
    )
    upload_button.click()
    time.sleep(2)  # 파일 선택창 대기

    # ---------------------------
    # 파일 선택창에 경로 입력
    # ---------------------------
    file_path = r"C:\Workspace\qa3team4\tests\upload_test.txt"  # raw string 사용
    pyautogui.write(file_path)
    pyautogui.press('enter')
    time.sleep(2)  # 업로드 처리 대기

    # ---------------------------
    # 업로드 완료 확인 (span 태그로 파일명 확인)
    # ---------------------------
    uploaded_file_name = os.path.basename(file_path)
    uploaded_file = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, f'//span[text()="{uploaded_file_name}"]')
        )
    )
    assert uploaded_file.is_displayed(), "파일 업로드 실패!"

    print("파일 업로드 테스트 완료!")
    

# ---------------------------
# 이미지 생성 테스트
# ---------------------------
def test_plus_image(driver):
    # 로그인
    login(driver, LOGIN_ID, LOGIN_PW, check_success=True)
    time.sleep(2)

    wait = WebDriverWait(driver, 10)

    # ---------------------------
    # 플러스 버튼 클릭 (업로드 메뉴 열기)
    # ---------------------------
    plus_button = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'button:has(svg[data-testid="plusIcon"])')
        )
    )
    plus_button.click()
    time.sleep(1)

    # ---------------------------
    # 파일 업로드 버튼 클릭
    # ---------------------------
    upload_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, '//span[text()="이미지 생성"]')
        )
    )
    upload_button.click()
    time.sleep(2)

    wait = WebDriverWait(driver, 10)

    image_generate_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, '//span[text()="이미지 생성"]')
        )
    )
    assert image_generate_button.is_displayed(), "이미지 생성 클릭 실패!"

    print("이미지 생성 테스트 완료!")
    
    
# ---------------------------
# 웹 검색 테스트
# ---------------------------
def test_plus_web(driver):
    # 로그인
    login(driver, LOGIN_ID, LOGIN_PW, check_success=True)
    time.sleep(2)

    wait = WebDriverWait(driver, 10)

    # ---------------------------
    # 플러스 버튼 클릭 (업로드 메뉴 열기)
    # ---------------------------
    plus_button = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'button:has(svg[data-testid="plusIcon"])')
        )
    )
    plus_button.click()
    time.sleep(1)

    # ---------------------------
    # 파일 업로드 버튼 클릭
    # ---------------------------
    upload_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, '//span[text()="웹 검색"]')
        )
    )
    upload_button.click()
    time.sleep(2)

    wait = WebDriverWait(driver, 10)

    
    image_generate_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, '//span[text()="웹 검색"]')
        )
    )
    assert image_generate_button.is_displayed(), "웹 검색 클릭 실패!"
        
    
