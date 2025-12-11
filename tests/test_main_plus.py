import pytest
import time
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys, os

# utils 경로 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.utils import login, logout
from utils.constants import LOGIN_ID, LOGIN_PW

# ---------------------------------------------------------------------------------
# 메시지 입력 창 좌측 "+" 버튼 클릭 기능 테스트
# ---------------------------------------------------------------------------------

# ---------------------------
# 파일 업로드 테스트
# ---------------------------
def test_plus_fileUpload(login_once):
    # 로그인
    #login(driver, LOGIN_ID, LOGIN_PW, check_success=True)
    driver = login_once
    time.sleep(2)

    wait = WebDriverWait(driver, 30)

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
    # 업로드할 파일 경로 생성
    # ---------------------------
    base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "tests")
    filenames = [
        "upload_test.txt",
        "upload_test.docx",
        "upload_test.pdf",
        "upload_test.png",
        "upload_test.jpg"
    ]

    # 파일 경로 → OS 파일선택창에서 여러 파일 선택 형식:  "경로1" "경로2" ...
    file_paths_string = ' '.join(
        f'"{os.path.join(base_dir, name)}"' for name in filenames
    )

    # ---------------------------
    # 파일 선택창에 여러 파일 경로 입력
    # ---------------------------
    pyautogui.write(file_paths_string)
    pyautogui.press('enter')
    time.sleep(3)  # 업로드 대기

    # ---------------------------
    # 각 파일 업로드 완료 확인
    # ---------------------------
    # ---------------------------
    # 각 파일 업로드 완료 확인
    # ---------------------------
    text_files = ["upload_test.txt", "upload_test.docx", "upload_test.pdf"]
    image_files = ["upload_test.png", "upload_test.jpg"]

    # 텍스트 계열 파일 확인 (span)
    for name in text_files:
        uploaded_file = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, f'//span[text()="{name}"]')
            )
        )
        #assert uploaded_file.is_displayed(), f"{name} 텍스트 파일 업로드 실패!"

    # 이미지 계열 파일 확인 (img alt)
    for name in image_files:
        uploaded_img = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, f'//img[@alt="{name}"]')
            )
        )
        #assert uploaded_img.is_displayed(), f"{name} 이미지 파일 업로드 실패!"
        
    #data-testid arrow-upIcon
    arrow = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'button:has(svg[data-testid="arrow-upIcon"])')
        )
    )
    arrow.click()
    
    complete_element = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, '//*[@data-status="complete"]')
        )
    )

    assert complete_element.is_displayed(), "업로드 완료 상태(data-status=complete)가 확인되지 않음"
        
    print("5개 파일 업로드 확인 완료!")

    

# ---------------------------
# 이미지 생성 테스트
# ---------------------------
def test_plus_image(login_once):
    # 로그인
    #login(driver, LOGIN_ID, LOGIN_PW, check_success=True)
    time.sleep(2)
    driver = login_once
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
def test_plus_web(login_once):
    # 로그인
    #login(driver, LOGIN_ID, LOGIN_PW, check_success=True)
    time.sleep(2)
    driver = login_once
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
        
    
