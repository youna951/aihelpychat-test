import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utils.common import clear_all
from selenium.webdriver.common.keys import Keys



class ChatHistoryPage:
    def __init__(self, logged_in_driver):
        driver = logged_in_driver
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # ==========================
    # 공통 요소/행동
    # ==========================
    def get_first_chat(self):
        chat_list = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'ul[data-testid="virtuoso-item-list"]'))
        )
        return chat_list.find_element(By.CSS_SELECTOR, 'a')

    def click_first_chat_menu(self):
        first_chat = self.get_first_chat()   # 첫 번째 항목 찾기
        first_chat.click()                   # 채팅 항목 자체 클릭          
    
    def open_menu(self, chat_element):
        """첫 번째 히스토리 항목 hover → 메뉴 클릭"""
        ActionChains(self.driver).move_to_element(chat_element).perform()
        time.sleep(0.2)
        ellipsis_icon = chat_element.find_element(By.CSS_SELECTOR, 'svg[data-icon="ellipsis-vertical"]')
        ellipsis_icon.click()

    def modal_closed(self, xpath):
        try:
            WebDriverWait(self.driver, 5).until(EC.invisibility_of_element_located((By.XPATH, xpath)))
            return True
        except TimeoutException:
            return False

    # ==========================
    # [채팅 히스토리] 채팅 히스토리 스크롤 확인 (AHCT-T150)
    # ==========================
    def check_history_visible(self):
        try:
            scroller = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="virtuoso-scroller"]'))
            )

            scroll_step = 500  # 한 번에 px 단위 스크롤
            last_total = 0

            while True:
                ui_container = scroller.find_element(By.CSS_SELECTOR, '[data-testid="virtuoso-item-list"]')
                items = ui_container.find_elements(By.TAG_NAME, "a")
                total_items = len(items)
                print("total_items:", total_items, flush=True)

                if total_items == 0:
                    print("[채팅 히스토리] a 태그가 없음", flush=True)
                    return False

                # scrollHeight 대비 scrollTop
                scroll_height = self.driver.execute_script("return arguments[0].scrollHeight", scroller)
                scroll_top = self.driver.execute_script("return arguments[0].scrollTop", scroller)
                client_height = self.driver.execute_script("return arguments[0].clientHeight", scroller)

                # 마지막까지 내려가면 break
                if scroll_top + client_height >= scroll_height:
                    break

                # 스크롤
                self.driver.execute_script(f"arguments[0].scrollBy(0, {scroll_step});", scroller)
                time.sleep(1)  # 렌더링 대기

            # 마지막 아이템 확인
            last_item = ui_container.find_elements(By.TAG_NAME, "a")[-1]
            print("last_item 텍스트:", last_item.text, flush=True)
            self.wait.until(lambda d: last_item.is_displayed())
            
            assert last_item.is_displayed(), "[채팅 히스토리] 마지막 아이템 화면에 표시되지 않음"

            print("[채팅 히스토리] 채팅 히스토리 스크롤 확인 (AHCT-T150) 성공!", flush=True)
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//ul[@data-testid="virtuoso-item-list"]')))
            return True
        except TimeoutException:
            print("[채팅 히스토리] 채팅 히스토리 스크롤 확인 (AHCT-T150) 실패 / check_history_visible")
            return False

    # --------------------------
    # [채팅 히스토리] 히스토리 타이틀 수정 - 정상 (AHCT-T151)
    # --------------------------
    def rename_history(self, new_title="이름변경 자동화 테스트"):
        try:
            first_chat = self.get_first_chat()
            self.open_menu(first_chat)

            rename_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "이름 변경")]'))
            )
            rename_btn.click()

            input_box = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'form input[type="text"]')))
            clear_all(input_box)
            input_box.send_keys(new_title)

            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "저장")]'))).click()

            try:
                self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="alert"]')))
                print("[채팅 히스토리] 히스토리 타이틀 수정 - 정상 (AHCT-T151) 성공!")
                return True
            except TimeoutException:
                print("[채팅 히스토리] 히스토리 타이틀 수정 - 정상 (AHCT-T151) 실패 / rename_history")
                return False
            
        except Exception as e:
            # Selenium 관련 다른 오류까지 모두 잡아서 출력
            print(f"[채팅 히스토리] 히스토리 타이틀 수정 - 정상 (AHCT-T151) ❌ 실패 / 예외 발생: {e}")
            return False

    # --------------------------
    # [채팅 히스토리] 히스토리 타이틀 수정 - 취소 (AHCT-T153)
    # --------------------------
    def rename_history_cancel(self):
        first_chat = self.get_first_chat()
        self.open_menu(first_chat)

        rename_btn = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "이름 변경")]'))
        )
        rename_btn.click()

        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "취소")]'))).click()

        if self.modal_closed('//h2[contains(text(), "이름 변경")]'):
            print("[채팅 히스토리] 히스토리 타이틀 수정 - 취소 (AHCT-T153) 성공!")
            return True
        else:
            print("[채팅 히스토리] 히스토리 타이틀 수정 - 취소 (AHCT-T153) 실패 / rename_history_cancel")
            return False

    # --------------------------
    # [채팅 히스토리] 히스토리 타이틀 삭제 - 정상 (AHCT-T152)
    # --------------------------
    def delete_history(self):
        first_chat = self.get_first_chat()
        self.open_menu(first_chat)

        delete_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//p[contains(text(), "삭제")]')))
        delete_btn.click()

        confirm_delete = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "삭제")]')))
        confirm_delete.click()

        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "대화가 삭제되었습니다!")]')))
            print("[채팅 히스토리] 히스토리 타이틀 삭제 - 정상 (AHCT-T152) 성공!")
            return True
        except TimeoutException:
            print("[채팅 히스토리] 히스토리 타이틀 삭제 - 정상 (AHCT-T152) 실패 / delete_history")
            return False

    # --------------------------
    # [채팅 히스토리] 히스토리 타이틀 삭제 - 취소 (AHCT-T154)
    # --------------------------
    def delete_history_cancel(self):
        first_chat = self.get_first_chat()
        self.open_menu(first_chat)

        delete_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//p[contains(text(), "삭제")]')))
        delete_btn.click()

        cancel_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "취소")]')))
        cancel_btn.click()

        if self.modal_closed('//h2[contains(text(), "삭제 확인")]'):
            print("[채팅 히스토리] 히스토리 타이틀 삭제 - 취소 (AHCT-T154) 성공!")
            return True
        else:
            print("[채팅 히스토리] 히스토리 타이틀 삭제 - 취소 (AHCT-T154) 실패 / delete_history_cancel")
            return False
        
    
    # --------------------------        
    # [채팅 히스토리] 히스토리 클릭시 전체 내용 조회 (AHCT-T155)
    # --------------------------
    def search_history_click(self): 
        self.driver.refresh()         
        self.click_first_chat_menu()
        
        complete_element = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, '//div[@data-status="complete"]')
            )
        )
        if complete_element.is_displayed():
            print("[채팅 히스토리] 히스토리 클릭시 전체 내용 조회 (AHCT-T155) 성공!")
            return True
        else:
            print("[채팅 히스토리] 히스토리 클릭시 전체 내용 조회 (AHCT-T155) 실패 / search_history_click")
            return False
        
        
    # --------------------------        
    #  [채팅 히스토리] 새 대화 버튼 클릭 - 초기화면에서 (AHCT-T156)
    # --------------------------
    def click_new_btn1(self):
        
        # 1. 대화 입력창 확인
        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, '//textarea[@name="input"]')
            )
        )
        
        # 2. 새 대화 클릭
        element = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//li//span[text()="새 대화"]')
            )
        )
        self.driver.execute_script(
            "arguments[0].click();", element
        )
        
        complete_element= self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, '//textarea[@name="input"]')
            )
        )
        
        if complete_element.is_displayed():
            print("[채팅 히스토리] 새 대화 버튼 클릭 - 초기화면에서 (AHCT-T156) 성공!")
            return True
        else:
            print("채팅 히스토리] 새 대화 버튼 클릭 - 초기화면에서 (AHCT-T156) 실패 / click_new_btn1")
            return False
    
    # --------------------------        
    # [채팅 히스토리] 새 대화 버튼 클릭 - 다른 히스토리 클릭 중 (AHCT-T157)
    # --------------------------
    def click_new_btn2(self):
        self.click_first_chat_menu()
        
        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, '//div[@data-status="complete"]')
            )
        )
        
        element = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//li//span[text()="새 대화"]')
            )
        )
        self.driver.execute_script(
            "arguments[0].click();", element
        )
                
        complete_element= self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, '//textarea[@name="input"]')
            )
        )
        
        if complete_element.is_displayed():
            print("[채팅 히스토리] 새 대화 버튼 클릭 - 다른 히스토리 클릭 중 (AHCT-T157) 성공!")
            return True
        else:
            print("[채팅 히스토리] 새 대화 버튼 클릭 - 다른 히스토리 클릭 중 (AHCT-T157) 실패 / click_new_btn2")
            return False
    
    
    
    # --------------------------        
    # [채팅 히스토리] 히스토리 검색 - 정상 조회 (AHCT-T158)
    # --------------------------
    def search_history_function(self):
        # "검색" 아이콘 클릭
        search_button = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//span[text()="검색"]')
            )
        )
        search_button.click()
        
        # try:
        #     # 특정 요소가 나타날 때까지 기다림
        #     search_modal = self.wait.until(
        #         EC.presence_of_element_located((By.CSS_SELECTOR, "div.MuiStack-root.css-j7qwjs"))
        #     )
        #     # ESC 키 전송
        #     ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
        # except TimeoutException:
        #     # 요소가 나타나지 않으면 무시
        #     history_scroll = self.wait.until(
        #         EC.invisibility_of_element_located((By.XPATH, '//ul[@data-testid="virtuoso-item-list"]'))
        #     )
            
        input_box = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="text"][placeholder="Search"]')))
        clear_all(input_box)
        input_box.send_keys("고양이")
        
        chat_list = self.wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'ul.MuiList-root.MuiList-padding')
            )
        )
        if chat_list.is_displayed():
            print("[채팅 히스토리] 히스토리 검색 - 정상 조회 (AHCT-T158) 성공!")
            return True
        else:
            print("[채팅 히스토리] 히스토리 검색 - 정상 조회 (AHCT-T158) 실패 / search_history_function")
            return False
        
        
    # --------------------------        
    # [채팅 히스토리] 히스토리 검색 - 검색 결과 없음 (AHCT-T159)
    # --------------------------
    def search_history_function_no_result(self):
        self.driver.refresh()
        # "검색" 아이콘 클릭
        search_button = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//span[text()="검색"]')
            )
        )
        search_button.click()
        
        input_box = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="text"][placeholder="Search"]')))
        clear_all(input_box)
        input_box.send_keys("python jenkins")
        
        try:
            no_result = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '//p[text()="검색 결과가 없습니다."]')
                )
            )
            if no_result.is_displayed():
                print("[채팅 히스토리] 히스토리 검색 - 검색 결과 없음 (AHCT-T159) 성공!")
                return True
            else:
                print("[채팅 히스토리] 히스토리 검색 - 검색 결과 없음 (AHCT-T159) 실패 / search_history_function_no_result")
                return False
        except TimeoutException:
            print('[채팅 히스토리] 히스토리 검색 - 검색 결과 없음 (AHCT-T159) 실패 / search_history_function_no_result')
            return False
        
        
    # --------------------------        
    # [채팅 히스토리] 히스토리 검색 - 취소 (AHCT-T160)
    # --------------------------
    def search_history_function_cancel(self):
        self.driver.refresh()
        # 검색 버튼 클릭
        search_button = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//span[text()="검색"]'))
        )
        search_button.click()

        # 모달 렌더링 기다림
        self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.MuiStack-root.css-j7qwjs'))
        )

        # X 버튼 클릭 (버튼 선택)
        self.wait.until(
            #EC.element_to_be_clickable((By.XPATH, '//button[./svg[@data-testid="xmarkIcon"]]'))
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button:has(svg[data-testid="xmarkIcon"])'))
        ).click()

        # 모달 사라짐 확인
        is_closed = self.modal_closed('div.MuiStack-root.css-j7qwjs')
        if is_closed:
            print("[채팅 히스토리] 히스토리 검색 - 취소 (AHCT-T160) 성공!")
            return True
        else:
            print("[채팅 히스토리] 히스토리 검색 - 취소 (AHCT-T160) 실패 / search_history_function_cancel")
            return False
    
    
    # --------------------------        
    # [채팅 히스토리] 메뉴 접기/펼치기 - 상단 ‘메뉴 아이콘’ 버튼 (AHCT-T161)
    # --------------------------
    def top_menu_off_on(self):
        # 1. 상단 메뉴 클릭
        self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button:has(svg[data-testid="barsIcon"])'))
        ).click()
        
        # 클릭 후 DOM 상태 갱신 (data-collapsible 값 확인)
        self.driver.execute_script(
            "return document.querySelector('aside[aria-hidden=\"false\"]').getAttribute('data-collapsible');"
        )
        
        # 2. 메뉴를 다시 클릭하여 접기
        self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button:has(svg[data-testid="barsIcon"])'))
        ).click()
        
        # 접힌 후 DOM 상태 갱신
        self.driver.execute_script(
            "return document.querySelector('aside[aria-hidden=\"false\"]').getAttribute('data-collapsible');"
        )
        
        # 메뉴가 펼쳐졌는지 확인
        top_menu_on = self.driver.execute_script(
            "return document.querySelector('aside[aria-hidden=\"false\"]').getAttribute('data-collapsible');"
        )
        
        if top_menu_on == "false":
            print("[채팅 히스토리] 메뉴 접기/펼치기 - 상단 ‘메뉴 아이콘’ 버튼 (AHCT-T161) 성공!")
            return True
        else:
            print("[채팅 히스토리] 메뉴 접기/펼치기 - 상단 ‘메뉴 아이콘’ 버튼 (AHCT-T161) 실패 / top_menu_off_on")
            return False

            
    
    # --------------------------        
    # [채팅 히스토리] 메뉴 접기/펼치기 - 하단 ‘메뉴 접기’ 버튼 (AHCT-T162)
    # --------------------------
    def bottom_menu_off_on(self):
        # 1. 하단 메뉴 클릭
        self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button:has(svg[data-testid="arrow-left-to-lineIcon"])'))
        ).click()
        
        # 클릭 후 DOM 상태 갱신 (data-collapsible 값 확인)
        self.driver.execute_script(
            "return document.querySelector('aside[aria-hidden=\"false\"]').getAttribute('data-collapsible');"
        )
        
        # 2. 메뉴를 다시 클릭하여 접기
        self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button:has(svg[data-testid="arrow-right-to-lineIcon"])'))
        ).click()
        
        # 접힌 후 DOM 상태 갱신
        self.driver.execute_script(
            "return document.querySelector('aside[aria-hidden=\"false\"]').getAttribute('data-collapsible');"
        )
        
        # 메뉴가 펼쳐졌는지 확인
        bottom_menu_on = self.driver.execute_script(
            "return document.querySelector('aside[aria-hidden=\"false\"]').getAttribute('data-collapsible');"
        )
        
        if bottom_menu_on == "false":
            print("[채팅 히스토리] 메뉴 접기/펼치기 - 하단 ‘메뉴 접기’ 버튼 (AHCT-T162) 성공!")
            return True
        else:
            print("[채팅 히스토리] 메뉴 접기/펼치기 - 하단 ‘메뉴 접기’ 버튼 (AHCT-T162) 실패 / top_menu_off_on")
            return False
    
    # --------------------------        
    # [채팅 히스토리] 메뉴 접기/펼치기 - 메뉴 자동 열림/닫힘 (AHCT-T163)
    # --------------------------
    def auto_menu_off_on(self):
        # 1. 상단 메뉴 클릭(숨기기)
        self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button:has(svg[data-testid="barsIcon"])'))
        ).click()
        
        # 2. 마우스 오버
        first_chat = self.get_first_chat()
        self.open_menu(first_chat)
        
        # 3. 펼친 후 DOM 상태 갱신
        auto_menu_on = self.driver.execute_script(
            "return document.querySelector('div[data-testid=\"virtuoso-scroller\"]').style.opacity;"
        )
        
        # 4. 메뉴가 펼쳐졌는지 확인
        if auto_menu_on == "1":
            print("[채팅 히스토리] 메뉴 접기/펼치기 - 메뉴 자동 열림/닫힘 (AHCT-T163) 성공!")
            return True
        else:
            print("[채팅 히스토리] 메뉴 접기/펼치기 - 메뉴 자동 열림/닫힘 (AHCT-T163) 실패 / auto_menu_off_on")
            return False