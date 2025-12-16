from selenium.webdriver.common.by import By
from utils.common import login, logout
from utils.constants import LOGIN_ID, LOGIN_PW
from pages.agent_search_page import AgentSearchPage
from pages.agent_builder_page import AgentBuilderPage

AI_Agent_name = "끝까지 간다"
TEST_DATA = "test_updated"

#     # =================================================
#     # AHCT-T20 에이전트 수정 페이지 이동 (에이전트 탐색)
#     # =================================================
#     # 에이전트 만들기 페이지로 이동

def test_agent_edit_inSearchPage(driver):
    login(driver, LOGIN_ID, LOGIN_PW)
    page_Search = AgentSearchPage(driver)
    page_Builder = AgentBuilderPage(driver)

    page_Search.open()
    # 챗봇 검색
    page_Search.type_query(AI_Agent_name)
    page_Search.assert_result_contains(AI_Agent_name)
    # ellipsis 버튼 클릭
    page_Search.click_ellipsis_for_agent(AI_Agent_name)
    # 편집 버튼 클릭
    page_Search.click_edit_menu()
    # 수정 페이지로 이동되었는지 확인
    page_Search.assert_edit_page_opened()
    
    logout(driver)