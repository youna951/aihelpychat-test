from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

class BasePage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def find(self, locator):
        return self.driver.find_element(*locator)

    def finds(self, locator):
        return self.driver.find_elements(*locator)

    def wait_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def wait_invisible(self, locator):
        return self.wait.until(EC.invisibility_of_element_located(locator))

    # 입력된 텍스트 지우기
    def clear_all(self, element):
        element.send_keys(Keys.CONTROL, 'a')
        element.send_keys(Keys.DELETE)
