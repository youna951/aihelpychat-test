from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC


class PptPage(BasePage):
    def __init__(self,driver):
        super().__init__(driver)
    # -------------------------------------
    # Locators
    # -------------------------------------
    TOOL_MENU = (By.XPATH, "//span[contains(text(),'도구')]")
    PPT_MENU = (By.XPATH, "//*[contains(text(),'PPT 생성')]")
    OVERLAY = (By.CSS_SELECTOR, ".MuiBackdrop-root")
    
    TITLE_INPUT = (By.NAME,"topic")
    INSTRUCTION_INPUT = (By.NAME,"instructions")
    SLIDE_INPUT = (By.NAME,"slides_count")
    SECTION_INPUT = (By.NAME,"section_count")
    TOGGLE_ONOFF = (By.NAME,"simple_mode")
    
    RECREATE_MODAL = (By.XPATH, "//div[contains(@class,'MuiDialog-root')]")
    RECREATE_BTN = (By.XPATH, "//div[contains(@class,'MuiDialog-root')]//button[.//text()='다시 생성']")
    CREATE_BTN = (By.XPATH, "//button[contains(text(),'생성')]")
    RECREATE_BTNS = (By.XPATH, "//button[contains(text(),'다시 생성')]")
    STOP_ICON = (By.XPATH, "//*[@data-testid='stopIcon']")
    STOP_BTN  = (By.XPATH, "//*[@data-testid='stopIcon']/ancestor::button")
    STOP_MSG = (By.XPATH, "//div[contains(text(),'요청에 의해 답변 생성을 중지했습니다.')]")
    # -------------------------------------
    # 페이지 이동
    # -------------------------------------
    def go_to_ppt(self):
        self.wait_clickable(self.TOOL_MENU).click()
        ppt_icon = self.wait.until(EC.visibility_of_element_located(self.PPT_MENU))
        ppt_icon.click()
    
    def is_ppt_page_opened(self):
        """PPT 생성 페이지에 도착했는지 여부"""
        return self.wait_visible(self.TITLE_INPUT).is_displayed()
    
    # -------------------------------------
    # 입력기능
    # -------------------------------------
    def input_title(self,text:str): #주제 입력
        self.wait_generation_closed()

        title_input = self.wait.until(
            EC.visibility_of_element_located(self.TITLE_INPUT)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", title_input
        )

        self.clear_all(title_input)
        title_input.send_keys(text)
    
    def input_instruction(self, text:str): #지시사항 입력
        el = self.find(self.INSTRUCTION_INPUT)
        self.clear_all(el)
        el.send_keys(text)
    
    def input_slide(self, text:str): #슬라이드 입력
        el = self.find(self.SLIDE_INPUT)
        self.clear_all(el)
        el.send_keys(text)
    
    def input_section(self, text:str): #섹션수 입력
        el = self.find(self.SECTION_INPUT)
        self.clear_all(el)
        el.send_keys(text)
    
    def toggle_onoff(self): #심층조사 모드 설정
        el = self.find(self.TOGGLE_ONOFF)
        el.click()
        
    def is_simple_mode_on(self):
        """스위치 ON 여부"""
        checkbox = self.find(self.TOGGLE_ONOFF)
        return checkbox.is_selected()
        
    # -------------------------------------
    # 상태
    # -------------------------------------
    def is_create_enabled(self):
        btn = self.find(self.CREATE_BTN)
        disabled = btn.get_attribute("disabled")
        return disabled is None
    
    def wait_button_state(self, expected: bool):
        """버튼 활성/비활성 변화를 기다림"""
        self.wait.until(
            lambda d: d.find_element(*self.CREATE_BTN).is_enabled() == expected
        )
    def get_slide_text(self):
        el = self.find(self.SLIDE_INPUT)
        return el.get_attribute("value")
    
    def get_section_text(self):
        el = self.find(self.SECTION_INPUT)
        return el.get_attribute("value")
    def is_stop_enable(self):
        return self.find(self.STOP_ICON_BTN).is_enabled()  
    
    def start_and_wait_for_stop_icon(self):
        """
        생성 → 다시 생성 → stop 아이콘 노출까지 수행
        성공 시 True / 실패 시 False
        """
        try:
            # 생성 클릭
            btn = self.find(self.CREATE_BTN)
            self.driver.execute_script("arguments[0].click();", btn)

            # 다시 생성 (두 번째 버튼)
            recreates = self.finds(self.RECREATE_BTNS)
            recreates[1].click()

            # stop 아이콘 등장 대기
            self.wait.until(EC.visibility_of_element_located(self.STOP_ICON))

            return True

        except NoSuchElementException:
            return False 
    
    # -------------------------------------
    # 생성 & 정지 기능
    # -------------------------------------
    def click_create(self):
        btn = self.wait.until(EC.visibility_of_element_located(self.CREATE_BTN))
        self.driver.execute_script("arguments[0].click();", btn)
        
    def click_stop(self):
        """
        생성 중 STOP 버튼 클릭
        - 아이콘이 '보일 때까지' 대기
        - 실제 클릭은 button에 수행
        """

        # 1️⃣ stop 아이콘이 화면에 보일 때까지 대기
        self.wait.until(EC.visibility_of_element_located(self.STOP_ICON))

        # 2️⃣ 실제 클릭 대상(button) 찾기
        stop_btn = self.find(self.STOP_BTN)

        # 3️⃣ 화면 중앙으로 이동 (애니메이션/가림 방지)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", stop_btn
        )

        # 4️⃣ JS 클릭 (MUI 안전 패턴)
        self.driver.execute_script("arguments[0].click();", stop_btn)

    def get_stop_message(self):
        return self.wait_visible(self.STOP_MSG).text
    
    def recreate_btn_click(self):
        # 1️⃣ 다시 생성 모달이 보일 때까지
        modal = self.wait.until(
            EC.visibility_of_element_located(self.RECREATE_MODAL)
        )

        # 2️⃣ 모달 안 '다시 생성' 버튼
        btn = modal.find_element(By.XPATH, ".//button[.//text()='다시 생성']")

        # 3️⃣ JS 클릭 (React 이벤트)
        self.driver.execute_script("arguments[0].click();", btn)

        # 4️⃣ 🔥 모달이 완전히 닫힐 때까지 기다림 (핵심)
        self.wait.until(
            EC.invisibility_of_element_located(self.RECREATE_MODAL)
        )
        
    def wait_generation_closed(self):
        """생성/진행 오버레이가 완전히 사라질 때까지 대기"""
        try:
            self.wait.until(EC.invisibility_of_element_located(self.OVERLAY))
        except:
            pass