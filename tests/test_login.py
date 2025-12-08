import time
import pytest
from selenium import webdriver
from selenium.common import ElementNotVisibleException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException


# ---------------------------
# Fixture : 브라우저 실행/종료
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

    # 테스트 종료 후 브라우저 닫기
    driver.quit()


# ---------------------------
# 실제 테스트
# ---------------------------
def test_login_success(driver):
    wait = WebDriverWait(driver, 10)
    url = "https://qaproject.elice.io/ai-helpy-chat"

    driver.get(url)
    time.sleep(1)

    # 로그인 ID 입력
    el_login_id = driver.find_element(By.NAME, "loginId")
    el_login_id.send_keys("qa3team04@elicer.com")

    time.sleep(1)

    # 로그인 PW 입력
    el_login_pw = driver.find_element(By.NAME, "password")
    el_login_pw.send_keys("20qareset25elice!")

    time.sleep(1)

    # 로그인 버튼 클릭
    driver.find_element(By.ID, ":r3:").click()
    time.sleep(2)

    try:
        textarea = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located(
        (By.XPATH, '//textarea[@placeholder="메시지를 입력하세요..."]')
    )
)
        assert textarea.is_displayed(), "로그인 후 textarea가 표시되지 않음"
    except NoSuchElementException:
        assert False, "로그인 실패: textarea 요소가 없음"

    print("로그인 성공 테스트 완료!")
    
    #//*[@id=":r1o:"]/div[2]/button[2]
    #/html/body/div[3]/div[3]/div[2]/div[2]/div[3]/div[2]/p
    #body > div.MuiDrawer-root.MuiDrawer-modal.MuiModal-root.css-1wutq42 > div.MuiPaper-root.MuiPaper-elevation.MuiPaper-elevation16.MuiDrawer-paper.MuiDrawer-paperAnchorBottom.css-a43l9p > div.MuiBox-root.css-1yw7e41 > div.MuiBox-root.css-0 > div:nth-child(7) > div.MuiListItemText-root.css-1lsm35k > p
    
    #로그아웃
    driver.find_element(By.XPATH, '//button[contains(@class, "css-1s53dya")]').click()
    logout_btn = driver.find_element(By.XPATH, '//p[contains(@class, "MuiTypography-root") and text()="로그아웃"]').click()
