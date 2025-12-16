from utils.common import login, logout
from utils.constants import LOGIN_ID, LOGIN_PW
from pages.agent_builder_page import AgentBuilderPage

PROMPT = "말 끝에 test라고 붙여야한다."
QUESTION = "안녕?"

    # =================================================
    # AHCT-T108 에이전트 규칙 직접 설정하기
    # =================================================
    # 에이전트 만들기 페이지로 이동
def test_agent_rule_settiing(driver):
    login(driver, LOGIN_ID, LOGIN_PW)

    page = AgentBuilderPage(driver)
    # 이름과 규칙 입력
    page.open_setting_tab()
    page.input_name(PROMPT)
    page.input_rules(PROMPT)
    # 미리보기 새로 고침
    page.refresh_preview()
    # 미리보기에 채팅 보내기
    page.input_preview_talk(QUESTION)
    page.preview_talk_send()
    #test로 끝나는지 확인
    page.assert_preview_answer()


    logout(driver)

#