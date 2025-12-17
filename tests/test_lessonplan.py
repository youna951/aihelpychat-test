import pytest
from pages.lessonplan_page import LessonPlanPage
from tests.data.lessonplan_test_data import *

class Test_Lesson_Plan:
    # -------------------------------------
    # AHCT-T56 수업지도안 페이지 정상 이동
    # -------------------------------------
    def test_go_lessonplan(self,login_once):
        page=LessonPlanPage(login_once)
        page.go_to_lessonplan()
        assert page.is_plan_page_opened(), "❌수업지도안 페이지로 이동하지 못함"
        print("✅ 수업지도안 페이지 이동 완료")
        
    # -------------------------------------
    # AHCT-T57 수업지도안 학교 드롭박스 내용 검증
    # -------------------------------------
    def test_school_dropdown(self, login_once):
        page = LessonPlanPage(login_once)
        school_level = page.get_dropdown_option("SCHOOL_DROPBOX")
        expexted_school = ["초등","중등","고등"] 
        assert school_level == expexted_school,(f"❌ 학교 선택 불일치 | 기대값={op}, 실제값={selected_value}")
        print("✅ 학교 드롭박스 학교 옵션 검증 완료")

    # --------------------------------------------------
    # AHCT-T00 수업지도안 학교 초등 선택시 학년 드롭박스 내용 검증
    # --------------------------------------------------
    def test_grade_dropdown_el(self,login_once):
        page = LessonPlanPage(login_once)
        page.select_el()
        grade_option = page.get_dropdown_option("GRADE_DROPBOX")
        expected_grades = ["1학년", "2학년", "3학년", "4학년", "5학년", "6학년"]
        assert grade_option == expected_grades,(f"❌ 학년 옵션 불일치 | 기대={expected_grades}, 실제={grade_option}")
        print("✅ 초등 선택 시 학년 드롭박스 검증 완료")
        #1학년 선택하게함.
        page.select_grade1()
    # --------------------------------------------------
    # AHCT-T00 수업지도안 학교 초등 선택시 과목 드롭박스 내용 검증
    # --------------------------------------------------
    def test_subject_dropdown_el(self,login_once):
        page = LessonPlanPage(login_once)
        page.select_el()
        subject_option = page.get_dropdown_option("SUBJECT_DROPBOX")
        expected_subject = [
            "국어","영어","수학","사회","과학","도덕","음악","미술","체육","실과"]
        assert subject_option == expected_subject,(f"❌ 과목 옵션 불일치 | 기대={expected_subject}, 실제={subject_option}")
        print("✅ 초등 선택 시 과목 드롭박스 검증 완료")
        #국어선택
        page.select_subject()
        
    # --------------------------------------------------
    # AHCT-T00 수업지도안 학교 중등 선택시 학년 드롭박스 내용 검증
    # --------------------------------------------------
    def test_grade_dropdown_mid(self,login_once):
        page = LessonPlanPage(login_once)
        page.select_mid()
        grade_option = page.get_dropdown_option("GRADE_DROPBOX")
        expected_grades = ["1학년", "2학년", "3학년"]
        assert grade_option == expected_grades,(f"❌ 학년 옵션 불일치 | 기대={expected_grades}, 실제={grade_option}")
        print("✅ 중등 선택 시 학년 드롭박스 검증 완료")
                #1학년 선택하게함.
        page.select_grade1()
    
    # --------------------------------------------------
    # AHCT-T00 수업지도안 학교 중등 선택시 과목 드롭박스 내용 검증
    # --------------------------------------------------
    def test_subject_dropdown_mid(self,login_once):
        page = LessonPlanPage(login_once)
        page.select_mid()
        subject_option = page.get_dropdown_option("SUBJECT_DROPBOX")
        expected_subject = [
            "국어","영어","수학","사회","과학","정보","도덕","기술·가정","음악","미술","체육"]
        assert subject_option == expected_subject,(f"❌ 과목 옵션 불일치 | 기대={expected_subject}, 실제={subject_option}")
        print("✅ 중등 선택 시 과목 드롭박스 검증 완료")
        #국어선택
        page.select_subject()
        
        
    # --------------------------------------------------
    # AHCT-T00 수업지도안 학교 고등 선택시 학년 드롭박스 내용 검증
    # --------------------------------------------------
    def test_grade_dropdown_high(self,login_once):
        page = LessonPlanPage(login_once)
        page.select_high()
        grade_option = page.get_dropdown_option("GRADE_DROPBOX")
        expected_grades = ["1학년", "2학년", "3학년"]
        assert grade_option == expected_grades,(f"❌ 학년 옵션 불일치 | 기대={expected_grades}, 실제={grade_option}")
        print("✅ 고등 선택 시 학년 드롭박스 검증 완료")
                #1학년 선택하게함.
        page.select_grade1()
    
    # --------------------------------------------------
    # AHCT-T00 수업지도안 학교 고등 선택시 과목 드롭박스 내용 검증
    # --------------------------------------------------
    def test_subject_dropdown_high(self,login_once):
        page = LessonPlanPage(login_once)
        page.select_high()
        subject_option = page.get_dropdown_option("SUBJECT_DROPBOX")
        expected_subject = [
            "국어","영어","수학","사회","과학","한국사","정보","제2외국어/한문","기술·가정","예술","체육"]
        assert subject_option == expected_subject,(f"❌ 과목 옵션 불일치 | 기대={expected_subject}, 실제={subject_option}")
        print("✅ 고등 선택 시 과목 드롭박스 검증 완료")
        #국어선택
        page.select_subject()
    
    # --------------------------------------------------
    # AHCT-T56 수업지도안 수업시간 드롭박스 유효성 검증
    # --------------------------------------------------
    def test_totaltime(self,login_once):
        page = LessonPlanPage(login_once)
        time_option = page.get_dropdown_option("CLASSTIME_DROPBOX")
        expected_time = [
            "40분","45분","50분"
        ]
        assert time_option == expected_time,(f"❌ 수업 시간 옵션 불일치 | 기대={expected_time}, 실제={time_option}")
        print("✅ 수업 시간 드롭박스 검증 완료")
        page.select_time()
        
    # ----------------------------------------------------------
    # AHCT-T61 수업지도안 성취기준 검색하기 버튼 클릭시 KICE페이지 이동
    # ----------------------------------------------------------
    def test_go_kice(self,login_once):
        page = LessonPlanPage(login_once)
        page.go_to_KICE() #assert Page안에 넣어줬습니다
        print("✅ 성취기준 사이트 새 창 검증 완료")
        
    # ----------------------------------------------------------
    # AHCT-T62 수업지도안 성취기준 입력 유효성 검증
    # ----------------------------------------------------------
    @pytest.mark.parametrize(
        "title,expected_enable,desc",
        LESSONPLAN_ACHIVEMENT_CASES
    )
    def test_input_achivement(self,login_once,title,expected_enable,desc):
        page = LessonPlanPage(login_once)
        page.input_achivement(title)
        actual = page.is_create_enabled()
        
        assert actual == expected_enable, (
            f"❌ 수업지도안 성취기준 {desc} 입력 시 생성 버튼 상태 불일치 | "
            f"기대={expected_enable}, 실제={actual}"
        )

        print(f"✅ 수업지도안 성취기준 {desc} 입력 → 생성 버튼 {'활성화' if expected_enable else '비활성화'}")

    # ----------------------------------------------------------
    # AHCT-T65 수업지도안 추가입력 입력 유효성 검증
    # ----------------------------------------------------------
    @pytest.mark.parametrize(
        "comment,expected_enable,desc",
        LESSONPLAN_COMMENT_CASES
    )
    def test_input_textarea(self,login_once,comment,expected_enable,desc):
        page = LessonPlanPage(login_once)
        page.input_textarea(comment)
        actual = page.is_create_enabled()

        assert actual == expected_enable, (
            f"❌ 수업지도안 코멘트 {desc} 입력 시 생성 버튼 상태 불일치 | "
            f"기대={expected_enable}, 실제={actual}"
        )

        print(f"✅ 수업지도안 코멘트 {desc} 입력 → 생성 버튼 {'활성화' if expected_enable else '비활성화'}")
    
    # ----------------------------------------------------------
    # AHCT-T00 수업지도안 입력 후 생성 버튼 클릭
    # ----------------------------------------------------------
    def test_createbtn(self,login_once):
        page = LessonPlanPage(login_once)
        page.input_achivement("4사03-02")
        page.click_create_button()
        page.click_recreate_button()
        assert page.is_stop_enable,"❌ 수업지도안 자동생성하고 있지 않음"
        print("✅수업지도안 생성 중입니다.")
        #다음 테스트를 위해 멈추어줌
        page.click_stop()
    
    # ----------------------------------------------------------
    # AHCT-T00 수업지도안 입력 후 정지 버튼 클릭
    # ----------------------------------------------------------
    def test_stopbtn(self,login_once):
        page = LessonPlanPage(login_once)
        page.click_create_button()
        page.click_recreate_button()
        page.click_stop()
        assert page.get_stop_message() == "요청에 의해 답변 생성을 중지했습니다."
        print("✅ 수업지도안 생성 중지 정상 동작")
    
    # ----------------------------------------------------------
    # AHCT-T00 수업지도안 성취기준 코드/기준 내용 검증
    # ----------------------------------------------------------
    @pytest.mark.parametrize(
        "input_value, expected_success, desc",
        LESSONPLAN_CODE_CASES
    )
    def test_achivement_code(self, login_once, input_value, expected_success, desc):
        page = LessonPlanPage(login_once)
        page.select_el()
        page.select_grade1()
        page.select_subject()
        page.input_achivement(input_value)
        page.click_create_button()
    
        if expected_success:
            page.click_recreate_button()
            result = page.wait_get_result()
            assert "수업 지도안을 생성했습니다" in result, (
                f"❌ 수업지도안 생성 실패 ({desc})"
            )
            print(f"✅ 수업지도안 생성 성공 ({desc})")
        else:
            assert not page.wait_get_result(), (
                f"✅ 유효하지 않은 값 생성 차단 확인 ({desc})"
            )
            print(f"❌ 유효하지 않은 값인데도 생성됨 ({desc})")
