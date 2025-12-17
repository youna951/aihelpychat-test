'''
작성자 : 이원기
'''

# tests/test_agent_chatbot_input.py
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import pyautogui
from pages.agent_builder_page import AgentBuilderPage
from utils.common import clear_all
import sys, os

# utils 경로 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


TEXT_OVER_100 = "1qfTqmBCWDK24DjpFicdK71cq9y0GPhpZfSxzmMHRkk3Es5EGn5h8CBD5W60aiMBXJLBWOtpXvuDzZSg9UTyLAzkmpkgMbyZ3b55a"
TEXT_ALIEN = "투늡은 디오자에서 은우꼐버으궀의"
TEXT_FOREIGN = "testテストทดสอบ"
TEXT_NORMAL = "NORMAL CHATBOT"


@pytest.fixture
def prepare_agent_chatbot_input(login_once):
    driver = login_once    
    return driver

@pytest.fixture
def agent_setting_page(prepare_agent_chatbot_input):
    driver = prepare_agent_chatbot_input
    wait = WebDriverWait(driver, 5)
    page = AgentBuilderPage(driver)
    page.open_setting_tab()

    return driver, wait, page

# ===============================================================
# [커스텀 에이전트][설정] 챗봇 이름 테스트
# - 100자 이상 입력 (비정상) (AHCT-T31)
# - 외계어 입력 (AHCT-T93)
# - 외국어 입력 (AHCT-T134)
# - 정상 입력 (AHCT-T30)
# ===============================================================
def test_chatbot_name(agent_setting_page):
    
    driver, wait, page = agent_setting_page
    
    test_cases = [
        (TEXT_OVER_100, True,  "[커스텀 에이전트][설정] 챗봇 이름 100자 이상 입력 (비정상) (AHCT-T31)"),
        (TEXT_ALIEN,    False, "[커스텀 에이전트][설정] 챗봇 이름 외계어 입력 (AHCT-T93)"),
        (TEXT_FOREIGN,  False, "[커스텀 에이전트][설정] 챗봇 이름 외국어 입력 (AHCT-T134)"),
        (TEXT_NORMAL,   False, "[커스텀 에이전트][설정] 챗봇 이름 입력 (정상) (AHCT-T30)"),
    ]

    for text, expect_error, test_case_id in test_cases:
        page.input_name(text)

        has_error = False
        error_text = ""

        try:
            error_el = wait.until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        '//input[@name="name"]'
                        '/ancestor::div[contains(@class,"MuiFormControl")]'
                        '//p[contains(@class,"Mui-error")]'
                    )
                )
            )
            has_error = True
            error_text = error_el.text

        except TimeoutException:
            has_error = False

        # ===================================================
        # 결과 로그 출력
        # ===================================================
        if has_error == expect_error:
            print(f"✅ [SUCCESS] {test_case_id}")
            if has_error:
                print(f"   └ 에러 메시지: {error_text}")
        else:
            print(f"❌ [FAIL] {test_case_id}")
            print(f"   └ 기대값: 에러 {'있음' if expect_error else '없음'}")
            print(f"   └ 실제값: 에러 {'있음' if has_error else '없음'}")
            if has_error:
                print(f"   └ 실제 에러 메시지: {error_text}")

        # pytest 판정
        assert has_error == expect_error, f"{test_case_id} 실패"

        # input 초기화
        el = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="name"]'))
        )
        clear_all(el)


# ===============================================================
# [커스텀 에이전트][설정] 챗봇 한줄소개 테스트 
# [커스텀 에이전트][설정] 챗봇 한줄 소개 300자 초과 입력 (비정상) (AHCT-T95)
# [커스텀 에이전트][설정] 챗봇 한줄 소개 입력 (정상) (AHCT-T94)
# ===============================================================
def test_chatbot_oneline(agent_setting_page):
    driver, wait, page = agent_setting_page
    page.input_name("NORMAL CHATBOT")
    TEXT_OVER_300 = "rXifAAkpUZcjG43ipkBLnUbf918s2GiFoQVM8QRKYeyTKPONm134J9w8n30Z0nL2vdcKEbeMkyItoCIG7DIYmBFsir3RQoxbJmj58qg7e4oftBrJ4mcypc4jd80pADAHWZbz7aW5thZqOAVex9PYFp5hjCkeCvLd1z4zn5tR4cT6VoAUpXYXmJ8zuMf85io1xWxLItVtMFGi3oQbg4GId6UlREmpM69BhCbzDp2f9snLHG3ohuPhD1ddwSMNutN54edV2mSf6fYdl16sPqDvVv35O0LpYkxroY4xgXoK205Jw"
    TEXT_NORMAL = "Test_description"
    
    test_cases = [
        (TEXT_OVER_300, True,  "[커스텀 에이전트][설정] 챗봇 한줄 소개 300자 초과 입력 (비정상) (AHCT-T95)"),
        (TEXT_NORMAL,   False, "[커스텀 에이전트][설정] 챗봇 한줄 소개 입력 (정상) (AHCT-T94)"),
    ]
    for text, expect_error, test_case_id in test_cases:
        page.input_description(text)

        has_error = False
        error_text = ""
    
        #description
        try:
            error_e2 = wait.until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        '//input[@name="description"]'
                        '/ancestor::div[contains(@class,"MuiFormControl")]'
                        '//p[contains(@class,"Mui-error")]'
                    )
                )
            )
            has_error = True
            error_text = error_e2.text

        except TimeoutException:
            has_error = False
            
        # ===================================================
        # 결과 로그 출력
        # ===================================================
        if has_error == expect_error:
            print(f"✅ [SUCCESS] {test_case_id}")
            if has_error:
                print(f"   └ 에러 메시지: {error_text}")
        else:
            print(f"❌ [FAIL] {test_case_id}")
            print(f"   └ 기대값: 에러 {'있음' if expect_error else '없음'}")
            print(f"   └ 실제값: 에러 {'있음' if has_error else '없음'}")
            if has_error:
                print(f"   └ 실제 에러 메시지: {error_text}")

        # pytest 판정
        assert has_error == expect_error, f"{test_case_id} 실패"

        # input 초기화
        el = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="description"]'))
        )
        clear_all(el)
        
        
# ===============================================================
# [커스텀 에이전트][설정] 챗봇 프로필
# [커스텀 에이전트][설정] 챗봇 프로필에 이미지 삽입(정상) (AHCT-T26)
# ===============================================================
def test_chatbot_img_upload(agent_setting_page):
    driver, wait, page = agent_setting_page
    '''
    <svg class="MuiSvgIcon-root MuiSvgIcon-fontSizeMedium EliceMuiEliceIcon-root epup0050 css-n25tio" focusable="false" aria-hidden="true" viewBox="0 0 448 512" data-fa="true" data-icon="plus" data-prefix="fas" data-unicode="2b" data-testid="plusIcon" svgPathWidth="20"><path d="M256 80c0-17.7-14.3-32-32-32s-32 14.3-32 32V224H48c-17.7 0-32 14.3-32 32s14.3 32 32 32H192V432c0 17.7 14.3 32 32 32s32-14.3 32-32V288H400c17.7 0 32-14.3 32-32s-14.3-32-32-32H256V80z"></path></svg>
    <li class="MuiButtonBase-root MuiMenuItem-root MuiMenuItem-gutters MuiMenuItem-root MuiMenuItem-gutters css-1mxhchc" tabindex="0" role="menuitem">사진 업로드</li>
    '''
    driver.find_element(By.CSS_SELECTOR, 'svg[data-testid="plusIcon"]').click()
    wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//li[contains(text(), "사진 업로드")]')
            )
    ).click()
    
    time.sleep(0.5)
    
    # ---------------------------
    # 업로드할 파일 경로 생성, 이미지 파일 업로드
    # ---------------------------
    base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "tests")
    filenames = [
        "upload_agent_test.png"
    ]
    # 파일 경로 → OS 파일선택창에서 여러 파일 선택 형식:  "경로1" "경로2" ...
    file_paths_string = ' '.join(
        f'"{os.path.join(base_dir, name)}"' for name in filenames
    )

    pyautogui.write(file_paths_string)
    pyautogui.press('enter')
    time.sleep(3)  # 업로드 대기
    
    uploaded_img = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'div.MuiAvatar-root img')
        )
    )
    if uploaded_img.is_displayed():
        print(f"✅ [SUCCESS] [커스텀 에이전트][설정] 챗봇 프로필에 이미지 삽입(정상) (AHCT-T26)")
    assert uploaded_img.is_displayed(), f"❌ [FAIL] [커스텀 에이전트][설정] 챗봇 프로필에 이미지 삽입(정상) (AHCT-T26)"
    
    
# ===============================================================
# [커스텀 에이전트][설정] 챗봇 프로필
# [커스텀 에이전트][설정] 챗봇 프로필에 이미지 생성기 기능 사용 (AHCT-T169)
# ===============================================================
def test_chatbot_img_create(agent_setting_page):
    driver, wait, page = agent_setting_page
    page.input_name("치와와")
    time.sleep(0.5)
    page.input_description("치와와")
    time.sleep(0.5)
    page.input_rules("치와와")
    time.sleep(0.5)
    
    wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, '//span[contains(text(), "저장됨")]')
        )
    )
    
    driver.find_element(By.CSS_SELECTOR, 'svg[data-testid="plusIcon"]').click()
    time.sleep(2)
    wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//li[contains(text(), "이미지 생성기")]')
            )
    ).click()
    time.sleep(10)
    uploaded_img = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'div.MuiAvatar-root img')
        )
    )
    if uploaded_img.is_displayed():
        print(f"✅ [SUCCESS] [커스텀 에이전트][설정] 챗봇 프로필에 이미지 생성기 기능 사용 (AHCT-T169)")
    assert uploaded_img.is_displayed(), f"❌ [FAIL] [커스텀 에이전트][설정] 챗봇 프로필에 이미지 생성기 기능 사용 (AHCT-T169)"