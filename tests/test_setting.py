import sys, os
import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 🔥 경로 추가 후 utils import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.utils import login, logout
from utils.constants import LOGIN_ID, LOGIN_PW

# ---------------------------
# 체크박스 클릭 함수(정상동작 하지 않음!!!)
# ---------------------------
def click_switch(driver, model_name, max_attempts=5):
    for attempt in range(1, max_attempts + 1):
        try:
            li_element = driver.find_element(By.XPATH, f'//li[.//span[text()="{model_name}"]]')
            switch_span = li_element.find_element(By.XPATH, './/span[contains(@class,"MuiSwitch-thumb")]/..')
            checkbox = li_element.find_element(By.XPATH, './/input[@type="checkbox"]')

            if checkbox.get_attribute("disabled"):
                print(f"⚠ {model_name} 체크박스는 disabled, 건너뜀")
                return

            # 화면 중앙으로 스크롤
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", switch_span)
            time.sleep(0.3)

            # 현재 상태 확인 (checked 기준)
            state = checkbox.get_attribute("checked") is not None
            print(f"{model_name} 현재 상태: {'ON' if state else 'OFF'}")

            # 클릭해서 상태 변경
            driver.execute_script("arguments[0].click();", checkbox)
            time.sleep(0.5)  # 클릭 후 안정화

            # 체크 여부 확인
            new_state = li_element.find_element(By.XPATH, './/input[@type="checkbox"]').get_attribute("checked") is not None
            if new_state != state:
                print(f"✔ {model_name} 상태 변경 성공: {'ON' if new_state else 'OFF'}")
                return
            else:
                print(f"⚠ {model_name} 시도 {attempt}: 상태 변경 실패, 재시도 중...")
                driver.refresh()
                time.sleep(1)

        except Exception as e:
            print(f"❌ {model_name} 시도 {attempt}: 에러 발생 - {e}")
            driver.refresh()
            time.sleep(1)
    print(f"❌ {model_name} 체크 실패!")

# ---------------------------
# 테스트 본문
# ---------------------------
def test_model_checkboxes(driver):
    # --- 로그인 / 설정 화면 이동 ---
    login(driver, LOGIN_ID, LOGIN_PW)
    time.sleep(2)  # 로그인 안정화

    # 설정 메뉴 이동
    driver.find_element(By.XPATH, '//*[@data-testid="gearIcon"]/ancestor::button').click()
    driver.find_element(By.XPATH, '//span[contains(text(), "설정")]').click()
    time.sleep(1)

    model_names = [
        "GPT-5.1",
        "GPT-5",
        "GPT-5 mini",
        "GPT-5 nano",
        "GPT-4.1",
        "GPT-4.1 mini",
        "Claude Sonnet 4.5",
        "Claude Sonnet 4",
        "Claude Haiku 4.5"
        # "Helpy Pro Agent"는 disabled이므로 제외
    ]

    for name in model_names:
        print(f"\n=== 모델 체크해제 테스트: {name} ===")
        click_switch(driver, name)

    print("\n🎉 모든 모델 체크해제 완료!")
    
    # 새 대화 > 모델 갯수 확인
    element = driver.find_element(By.XPATH, '//li//span[text()="새 대화"]')
    driver.execute_script("arguments[0].click();", element)

    time.sleep(1)
    element = driver.find_element(By.XPATH, '//p[contains(text(),"Helpy Pro Agent")]')
    driver.execute_script("arguments[0].click();", element)

    lis = driver.find_elements(By.XPATH, '//li[contains(@class,"MuiMenuItem-root")]')
    print(len(lis))
    
    # 모델 설정 메뉴 이동    
    driver.find_element(By.XPATH, '//span[contains(text(), "모델 설정")]').click()
    time.sleep(1)

    for name in model_names:
        print(f"\n=== 모델 체크 테스트: {name} ===")
        click_switch(driver, name)
    
    # 새 대화 > 모델 갯수 확인
    element = driver.find_element(By.XPATH, '//li//span[text()="새 대화"]')
    driver.execute_script("arguments[0].click();", element)

    time.sleep(1)
    element = driver.find_element(By.XPATH, '//p[contains(text(),"Helpy Pro Agent")]')
    driver.execute_script("arguments[0].click();", element)
    
    lis = driver.find_elements(By.XPATH, '//li[contains(@class,"MuiMenuItem-root")]')
    print(len(lis))
    
    assert len(lis) == 10, f"모델 개수는 10이어야 합니다. 현재: {len(lis)}"
    print("\n🎉 모든 모델 체크 완료!")