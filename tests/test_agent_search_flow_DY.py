from utils.common import login, logout
from utils.constants import LOGIN_ID, LOGIN_PW
from pages.agent_search_page import AgentSearchPage

    # =================================================
    # AHCT-T19 에이전트 조회 기능 (성공)
    # =================================================
def test_agent_search_success(driver):
    login(driver, LOGIN_ID, LOGIN_PW)

    page = AgentSearchPage(driver)
    page.open().type_query("엘리스 온보딩 챗봇").assert_result_contains("엘리스 온보딩 챗봇")

    logout(driver)


    # =================================================
    # AHCT-T166 에이전트 조회 기능 (실패)
    # =================================================
def test_agent_search_fail_no_result(driver):
    login(driver, LOGIN_ID, LOGIN_PW)

    page = AgentSearchPage(driver)
    page.open().type_query("엘리스 오프로딩 챗봇").assert_no_result_contains("검색 결과가 없습니다.")

    logout(driver)

    # 