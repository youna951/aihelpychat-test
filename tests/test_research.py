import pytest
from pages.research_page import ResearchPage

class TestResearch:
    # -------------------------------------------- 
    # AHCT-T85 심층조사 페이지 정상이동 
    # --------------------------------------------
    def test_godeepdive(self, login_once):
        page = ResearchPage(login_once)
        page.go_to_research()
        print("✅ 심층 조사 페이지 이동 완료")
    # -------------------------------------------- 
    # AHCT-T86 심층조사 주제 입력 유효성 검증
    # -------------------------------------------- 
    def test_research_title(self, login_once):
        page = ResearchPage(login_once)

        # 공백
        page.input_title("")
        assert not page.is_create_enabled()
        print("✅공백 입력 → 생성 버튼 비활성화됨")

        # 1글자
        page.input_title("가")
        assert page.is_create_enabled()

        # 500자
        page.input_title("가" * 500)
        assert page.is_create_enabled()

        # 501자
        page.input_title("가" * 501)
        assert not page.is_create_enabled()
    # -------------------------------------------- 
    # AHCT-T88 심층조사 지시사항 입력 
    # --------------------------------------------
    def test_instruction(self, login_once):
        page = ResearchPage(login_once)
        page.input_title("가")
        # 공백
        page.input_instruction("")
        assert page.is_create_enabled(),"[심층조사] 지시사항이 비어있는데 생성 버튼이 활성화 됨"

        # 2000자
        page.input_instruction("가" * 2000)
        assert page.is_create_enabled(),"[심층조사] 지시사항이 2000자 인데 생성버튼이 활성화 됨"

        # 2001자
        page.input_instruction("가" * 2001)
        assert not page.is_create_enabled(),"[심층조사] 지시사항이 2001자 이상인데 생성버튼 비활성화 됨"
    # -------------------------------------------- 
    # AHCT-T00 심층조사 생성 중지 버튼 
    # --------------------------------------------
    def test_research_stop(self, login_once):
        page = ResearchPage(login_once)

        page.input_title("강아지")
        page.input_instruction("강아지 종에 대해 알려줘")
        page.click_create()
        page.recreate_btn_click()
        page.click_stop()

        assert page.get_stop_message() == "요청에 의해 답변 생성을 중지했습니다."
        print("✅ 정지 버튼 테스트 완료")
