from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class AgentSearchPage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # =================================================
    # 공통 유틸
    # =================================================
    def safe_click(self, el):
        try:
            el.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", el)

    # =================================================
    # 페이지 이동 및 조작
    # =================================================
    # 메뉴 - 에이전트 탐색 이동
    def open(self):
        menu = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//span[normalize-space(text())="에이전트 탐색"]/ancestor::li'))
        )
        menu.click()
        return self

    # 검색창 입력
    def type_query(self, text: str):
        search_input = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[placeholder="AI 에이전트 검색"]'))
        )
        search_input.clear()
        search_input.send_keys(text)
        return self

    # =================================================
    # ellipsis 메뉴 (카드 스코프)
    # =================================================
    # 에이전트 탐색 페이지에서 ellipsis 버튼 누르기 (메뉴 열기만)
    def click_ellipsis_for_agent(self, agent_title: str, timeout=30):
        import time
        wait = WebDriverWait(self.driver, timeout)
        card_xpath = f'//a[.//*[self::p or self::span][contains(normalize-space(.), "{agent_title}")]]'
        
        # 검색 결과 안정화 대기
        time.sleep(0.5)
        
        # 1) 카드 찾기
        card = wait.until(EC.presence_of_element_located((By.XPATH, card_xpath)))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", card)

        # 2) hover
        ActionChains(self.driver).move_to_element(card).pause(0.3).perform()

        # 3) 카드 다시 찾기 (stale 방지)
        card = self.driver.find_element(By.XPATH, card_xpath)
        
        # 4) 버튼 찾기
        ellipsis_btn = card.find_element(By.CSS_SELECTOR, 'button:has(svg[data-testid="ellipsis-verticalIcon"])')
        self.safe_click(ellipsis_btn)

        # 5) 메뉴 등장 대기
        wait.until(EC.visibility_of_element_located((
            By.XPATH, '//ul//li//*[self::span or self::p][normalize-space(.)="편집"]'
        )))
        return self

    # =================================================
    # 메뉴 항목 클릭 (메뉴 스코프) - ellipsis 클릭 후 사용
    # =================================================
    # 편집 클릭
    def click_edit_menu(self, timeout=10):
        wait = WebDriverWait(self.driver, timeout)
        edit_btn = wait.until(EC.element_to_be_clickable((
            By.XPATH, '//ul//li//*[self::span or self::p][normalize-space(.)="편집"]'
        )))
        edit_btn.click()
        return self

    # 삭제 클릭
    def click_delete_menu(self, timeout=10):
        wait = WebDriverWait(self.driver, timeout)
        delete_btn = wait.until(EC.element_to_be_clickable((
            By.XPATH, '//ul//li//*[self::span or self::p][normalize-space(.)="삭제"]'
        )))
        delete_btn.click()
        return self

    # =================================================
    # 검증 
    # =================================================
    # 결과 검증: 결과 영역에서 text 포함되는 요소가 하나라도 있으면 PASS
    def assert_result_contains(self, text: str):
        self.wait.until(lambda d: text in d.page_source)
        assert text in self.driver.page_source, f'검색 결과에서 "{text}"를 찾지 못함'
        return self

    def assert_no_result_contains(self, text: str):
        el = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "h6.MuiTypography-subtitle1"))
        )
        assert "검색 결과가 없습니다." in el.text
        return self

    # 에이전트 편집을 눌러서 편집 페이지로 왔는지 검증
    def assert_edit_page_opened(self, timeout=10):
        btn = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located((By.XPATH, '//button[normalize-space(.)="업데이트"]'))
        )
        assert btn.is_displayed(), "업데이트 버튼이 보이지 않음 - 편집 페이지 진입 실패"
        return self