import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys, os


# utils 경로 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.common import login, logout
from utils.constants import LOGIN_ID, LOGIN_PW

# ---------------------------
# 단어형 입력 (AHCT-T104)
# ---------------------------

def test_word_input(login_once):
    time.sleep(2)
    driver = login_once
    wait = WebDriverWait(driver, 10)

     # 1. 입력창 찾기
    input_box = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'textarea[placeholder="메시지를 입력해 주세요."]')
        )
    )

    # 2. 입력창에 단어 입력
    test_message = "사과"
    input_box.send_keys(test_message)

    time.sleep(3)

     # 3. 보내기 버튼 클릭
    send_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[@type='button' and @aria-label='보내기']")
        )
    )
    send_button.click()

    time.sleep(3)

    # 4. 전송된 메시지가 UI에 나타나는지 확인
    sent_message = wait.until(
        EC.visibility_of_element_located(
            # 화면에 표시되는 단어와 입력한 단어가 같은지 확인
            (By.XPATH, f"//span[@data-status='complete' and text()='{test_message}']")
        )
    )

    time.sleep(3)

    # 5. 답장이 왔는지만 확인 (내용 무시)
    reply = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '[data-status="complete"]')
    )
)

    assert reply is not None
    assert reply.text.strip() != ""
    print("단어형 텍스트 입력 테스트 완료!")


# ---------------------------
# 문자형 입력 (AHCT-T104)
# ---------------------------

def test_sentence_input(login_once):
    time.sleep(2)
    driver = login_once
    wait = WebDriverWait(driver, 10)


     # 1. 입력창 찾기
    input_box = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'textarea[placeholder="메시지를 입력해 주세요."]')
        )
    )

    # 2. 입력창에 단어 입력
    test_message = "이삭 맛있다 냠냠"
    input_box.send_keys(test_message)

    time.sleep(3)

     # 3. 보내기 버튼 클릭
    send_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[@type='button' and @aria-label='보내기']")
        )
    )
    send_button.click()

    time.sleep(3)

    # 4. 전송된 메시지가 UI에 나타나는지 확인
    sent_message = wait.until(
        EC.visibility_of_element_located(
            # 화면에 표시되는 단어와 입력한 단어가 같은지 확인
            (By.XPATH, f"//span[@data-status='complete' and text()='{test_message}']")
        )
    )

    time.sleep(3)

    # 5. 답장이 왔는지만 확인 (내용 무시)
    reply = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '[data-status="complete"]')
    )
)

    assert reply is not None
    assert reply.text.strip() != ""
    print("문장형 텍스트 입력 테스트 완료!")

# ---------------------------
# 외국어 입력 (AHCT-T23)
# ---------------------------

@pytest.mark.parametrize(
    "test_message",
    [
        "Hello, how are you?",         # 영어
        "你好，你怎么样？"             # 중국어
    ]
)

def test_foreign_input(login_once,test_message):
    time.sleep(2)
    driver = login_once
    wait = WebDriverWait(driver, 10)


     # 1. 입력창 찾기
    input_box = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'textarea[placeholder="메시지를 입력해 주세요."]')
        )
    )

    # 2. 입력창에 단어 입력
    input_box.send_keys(test_message)

    time.sleep(3)

     # 3. 보내기 버튼 클릭
    send_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[@type='button' and @aria-label='보내기']")
        )
    )
    send_button.click()

    time.sleep(3)

    # 4. 전송된 메시지가 UI에 나타나는지 확인
    sent_message = wait.until(
        EC.visibility_of_element_located(
            # 화면에 표시되는 단어와 입력한 단어가 같은지 확인
            (By.XPATH, f"//span[@data-status='complete' and text()='{test_message}']")
        )
    )

    time.sleep(3)

    # 5. 답장이 왔는지만 확인 (내용 무시)
    reply = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '[data-status="complete"]')
    )
)

    assert reply is not None
    assert reply.text.strip() != ""
    print("외국어 텍스트 입력 테스트 완료!")

# ---------------------------
# 엉망인 띄어쓰기, 오타 입력 (AHCT-T103)
# ---------------------------

@pytest.mark.parametrize(
    "test_message",
    [
        "우리나라대통령누구야",  # 띄어쓰기 x
        "우리 나 라대 통 령 누구 야", # 엉망인 띄어쓰기
        "우리냐라 데퉁령 누구야" # 오타가 포함된
    ]
)

def test_messy_input(login_once,test_message):
    time.sleep(2)
    driver = login_once
    wait = WebDriverWait(driver, 10)


     # 1. 입력창 찾기
    input_box = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'textarea[placeholder="메시지를 입력해 주세요."]')
        )
    )

    # 2. 입력창에 단어 입력
    input_box.send_keys(test_message)

    time.sleep(3)

     # 3. 보내기 버튼 클릭
    send_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[@type='button' and @aria-label='보내기']")
        )
    )
    send_button.click()

    time.sleep(3)

    # 4. 전송된 메시지가 UI에 나타나는지 확인

    sent_message = wait.until(
        EC.visibility_of_element_located(
            # 화면에 표시되는 단어와 입력한 단어가 같은지 확인
            (By.XPATH, f"//span[@data-status='complete' and text()='{test_message}']")
        )
    )

    time.sleep(3)

    # 5. 답장이 왔는지만 확인 (내용 무시)
    wait = WebDriverWait(driver, 30)  # 30초까지 기다림
    
    reply = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '[data-status="complete"]')
    )
)

    assert reply is not None
    assert reply.text.strip() != ""
    print("엉망인 띄어쓰기, 오타 입력 테스트 완료!")


    

# ---------------------------
# 엄청 긴 문자열 입력 (AHCT-T28)
# ---------------------------

def test_long_sentence_input(login_once):
    time.sleep(2)
    driver = login_once
    wait = WebDriverWait(driver, 10)


     # 1. 입력창 찾기
    input_box = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'textarea[placeholder="메시지를 입력해 주세요."]')
        )
    )


    # 2. 입력창에 긴 텍스트 파일에서 텍스트를 가져와서 입력

    file_path = os.path.join(os.path.dirname(__file__), "long_text.txt")
    with open("long_text.txt", "r", encoding="utf-8") as f:
        test_message = f.read()

    # 500자씩 나눠서 입력
    chunk_size = 500
    text = test_message.replace("\n", " ")  # 줄바꿈 제거
    for i in range(0, len(text), chunk_size):
        input_box.send_keys(text[i:i+chunk_size])
    time.sleep(3)



     # 3. 보내기 버튼 클릭
    send_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[@type='button' and @aria-label='보내기']")
        )
    )
    send_button.click()

    time.sleep(3)


    # 5. 답장이 왔는지만 확인 (내용 무시)
    reply = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '[data-status="complete"]')
    )
)

    assert reply is not None
    assert reply.text.strip() != ""
    print("엄청 긴 문자열 텍스트 입력 테스트 완료!")



    


