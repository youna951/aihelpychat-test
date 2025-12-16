import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class AgentBuilderPage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # =================================================
    # 이동
    # =================================================
        #에이전트 탐색 클릭
    def open_setting_tab(self):
        # NOTE: 지침이 CSS 우선이지만, 메뉴 텍스트 기반 클릭은 현재 DOM에서 XPath가 제일 안정적일 수 있음.
        # 이후 Sidebar 컴포넌트로 빼면서 CSS-only + text filter 방식으로 전환 가능.
        agent_menu = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//span[text()="에이전트 탐색"]/ancestor::li'))
        )
        agent_menu.click()
        #+ 만들기 클릭 
        create_btn = self.wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'a[href="/ai-helpy-chat/agents/builder"]')
            )
        )
        create_btn.click()
        # 설정 클릭
        setting_tab = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "설정")]'))
        )
        setting_tab.click()
        return self

    # =================================================
    # 입력
    # =================================================
        #챗봇 이름
    def input_name(self, text):
        el = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="name"]'))
        )
        el.clear()
        el.send_keys(text)
        return self
        #한줄 소개
    def input_description(self, text):
        el = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="description"]'))
        )
        el.clear()
        el.send_keys(text)
        return self
        #규칙
    def input_rules(self, text):
        el = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'textarea[name="systemPrompt"]'))
        )
        el.clear()
        el.send_keys(text)
        return self
        #시작 대화 1~4
    def input_starter(self, index: int, text: str):
        css = f'input[name="conversationStarters.{index}.value"]'
        el = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, css))
        )
        el.clear()
        el.send_keys(text)
        return self

    # =================================================
    # 미리보기
    # =================================================
    # 미리보기 새로고침 버튼 클릭
    def refresh_preview(self):
        btn = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="새로고침"]'))
        )
        btn.click()
        return self
    
    # =================================================
    # 미리보기에 채팅 입력하기
    # =================================================
    # 미리보기에 채팅 입력
    def input_preview_talk(self, text: str):
        def _get_preview_textarea(d):
            els = d.find_elements(By.CSS_SELECTOR, 'textarea[name="input"]')
            print("textarea[name=input] 개수:", len(els))
            print("보이는 개수:", len([e for e in els if e.is_displayed()]))
            visible = [e for e in els if e.is_displayed() and e.is_enabled()]
            return visible[-1] if visible else False

        el = self.wait.until(_get_preview_textarea)
        el.clear()
        el.send_keys(text)
        return self

    # 미리보기 채팅 입력 보내기
    def preview_talk_send(self):
        def _get_preview_send_btn(d):
            btns = d.find_elements(By.CSS_SELECTOR, 'button[aria-label="보내기"]')
            clickable = [b for b in btns if b.is_displayed() and b.is_enabled()]
            return clickable[-1] if clickable else False

        btn = self.wait.until(_get_preview_send_btn)
        btn.click()
        return self


    # =================================================
    # 검증 - input 값 기준(안정적)
    # =================================================
    #이름 검증
    def assert_name_input_value(self, expected):
        el = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="name"]'))
        )
        value = el.get_attribute("value") or ""
        assert expected in value, f"이름 input에 '{expected}' 없음: 실제값={value}"
    #한줄 소개 검증
    def assert_description_input_value(self, expected):
        el = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="description"]'))
        )
        value = el.get_attribute("value") or ""
        assert expected in value, f"한줄 소개 input에 '{expected}' 없음: 실제값={value}"
    #규칙 검증
    def assert_rules_input_value(self, expected):
        el = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'textarea[name="systemPrompt"]'))
        )
        value = el.get_attribute("value") or ""
        assert expected in value, f"규칙 textarea에 '{expected}' 없음: 실제값={value}"

    # =================================================
    # 검증 - 미리보기 기준(불안정할 수 있어 DEBUG 포함)
    # =================================================
    def assert_preview_name(self, expected):
        # 기존 네 코드에서 사용하던 h6 기반(다만 class는 자주 바뀔 수 있음)
        title = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "h6.MuiTypography-h6"))
        )
        assert expected in title.text, f'이름 미리보기 불일치: 실제="{title.text.strip()}"'

    def assert_preview_description(self, expected, debug=True):
        ps = self.driver.find_elements(By.CSS_SELECTOR, "p.MuiTypography-body1")
        texts = [p.text.strip() for p in ps if p.text and p.text.strip()]
        if debug:
            print("\n[DEBUG] p.MuiTypography-body1 count =", len(texts))
            for i, t in enumerate(texts[:40], start=1):
                print(f"[DEBUG body1 {i}] {t}")
        assert any(expected in t for t in texts), (
            f'미리보기(추정)에서 "{expected}"를 찾지 못함. '
            f"(현재는 p.MuiTypography-body1 전체에서 검색 중)"
        )

    def assert_preview_starter(self, text, debug=False):
        # 시작 대화는 보통 미리보기 버튼 span에 들어감(기존 접근 유지)
        spans = self.driver.find_elements(By.CSS_SELECTOR, "button span")
        span_texts = [s.text.strip() for s in spans if s.text and s.text.strip()]
        if debug:
            print("\n[DEBUG] button span count =", len(span_texts))
            for i, t in enumerate(span_texts[:60], start=1):
                print(f"[DEBUG span {i}] {t}")
        assert any(text in t for t in span_texts), f'미리보기 시작 대화 "{text}" 없음'
    
    # 답변이 test로 끝나는지
    def assert_preview_answer(self, timeout=20):
        def _answer_endswith_test(d):
            answers = d.find_elements(By.CSS_SELECTOR, "p.css-dmwv96.e1d5acfy0")
            texts = [a.text.strip() for a in answers if a.text and a.text.strip()]
            return any(t.endswith("test") for t in texts)

        try:
            WebDriverWait(self.driver, timeout).until(_answer_endswith_test)
        except TimeoutException:
            answers = self.driver.find_elements(By.CSS_SELECTOR, "p.css-dmwv96.e1d5acfy0")
            texts = [a.text.strip() for a in answers if a.text and a.text.strip()]
            assert False, f"{timeout}초 안에 test로 끝나는 답변이 나오지 않음. 현재 답변={texts}"