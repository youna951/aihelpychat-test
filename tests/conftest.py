import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# utils import
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.utils import login
from utils.constants import LOGIN_ID, LOGIN_PW


#########################################
# 기본 WebDriver Fixture
#########################################
@pytest.fixture
def driver():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    #chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--window-size=1440,1280")
    chrome_options.add_argument("--window-position=0,0")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(5)

    yield driver
    driver.quit()



#########################################
# 로그인된 상태가 필요한 테스트를 위한 Fixture
#########################################
@pytest.fixture
def logged_in_driver(driver):
    """로그인이 필요한 테스트용 Fixture"""
    login(driver, LOGIN_ID, LOGIN_PW, check_success=True)
    time.sleep(1)
    return driver
