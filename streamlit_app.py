import streamlit as st
import math

# 페이지 설정
st.set_page_config(page_title="체력시험 합격 판정 시스템", layout="wide")

# 세션 상태 초기화
if 'page' not in st.session_state:
    st.session_state.page = "university_select"
if 'gender' not in st.session_state:
    st.session_state.gender = None
if 'selected_university' not in st.session_state:
    st.session_state.selected_university = None
if 'naesin_score' not in st.session_state:
    st.session_state.naesin_score = None
if 'practical_scores' not in st.session_state:
    st.session_state.practical_scores = {}

# 대학별 기준 데이터
UNIVERSITY_STANDARDS = {
    "가천대학교": {
        "naesin_max": 300,
        "practical_max": 700,
        "male": {
            "배근력검사": {"standard": 221, "max_score": 175, "unit": "kg", "decreasing": False, "per_grade": 5, "score_per_grade": 8.75},
            "10m왕복달리기": {"standard": 8.00, "max_score": 175, "unit": "초", "decreasing": True, "per_grade": 0.1, "score_per_grade": 8.75},
            "제자리멀리뛰기": {"standard": 300, "max_score": 175, "unit": "cm", "decreasing": False, "per_grade": 5, "score_per_grade": 8.75},
            "메디신볼던지기": {"standard": 12.5, "max_score": 175, "unit": "m", "decreasing": False, "per_grade": 0.2, "score_per_grade": 8.75}
        },
        "female": {
            "배근력검사": {"standard": 161, "max_score": 175, "unit": "kg", "decreasing": False, "per_grade": 5, "score_per_grade": 8.75},
            "10m왕복달리기": {"standard": 9.20, "max_score": 175, "unit": "초", "decreasing": True, "per_grade": 0.1, "score_per_grade": 8.75},
            "제자리멀리뛰기": {"standard": 240, "max_score": 175, "unit": "cm", "decreasing": False, "per_grade": 5, "score_per_grade": 8.75},
            "메디신볼던지기": {"standard": 9.8, "max_score": 175, "unit": "m", "decreasing": False, "per_grade": 0.2, "score_per_grade": 8.75}
        }
    },
    "상명대학교": {
        "naesin_max": 300,
        "practical_max": 700,
        "male": {
            "제자리멀리뛰기": {"standard": 305, "max_score": 245, "unit": "cm", "decreasing": False, "per_grade": 3, "score_per_grade": 17.5},
            "메디신볼던지기": {"standard": 12.7, "max_score": 210, "unit": "m", "decreasing": False, "per_grade": 0.2, "score_per_grade": 15},
            "20m왕복달리기": {"standard": 15.0, "max_score": 245, "unit": "초", "decreasing": True, "per_grade": 0.2, "score_per_grade": 17.5}
        },
        "female": {
            "제자리멀리뛰기": {"standard": 250, "max_score": 245, "unit": "cm", "decreasing": False, "per_grade": 3, "score_per_grade": 17.5},
            "메디신볼던지기": {"standard": 10.4, "max_score": 210, "unit": "m", "decreasing": False, "per_grade": 0.2, "score_per_grade": 15},
            "20m왕복달리기": {"standard": 16.4, "max_score": 245, "unit": "초", "decreasing": True, "per_grade": 0.2, "score_per_grade": 17.5}
        }
    }
}

# 표시용 이름 및 로고
DISPLAY_NAMES = {"가천대학교": "가천대학교 체육학부", "상명대학교": "상명대학교 스포츠건강관리전공"}
DISPLAY_LOGOS = {
    "가천대학교": "https://z-one.kr/_next/image?url=%2Fimages%2Funiversity%2F%EA%B0%80%EC%B2%9C%EB%8C%80%ED%95%99%EA%B5%90.webp&w=64&q=75",
    "상명대학교": "https://z-one.kr/_next/image?url=%2Fimages%2Funiversity%2F%EC%83%81%EB%AA%85%EB%8C%80%ED%95%99%EA%B5%90.webp&w=64&q=75"
}


def calculate_practical_score(event_name, performance, university="가천대학교", gender="남자"):
    gender_key = "male" if gender == "남자" else "female"
    standards = UNIVERSITY_STANDARDS[university][gender_key][event_name]

    standard = standards["standard"]
    max_score = standards["max_score"]
    is_decreasing = standards["decreasing"]
    per_grade = standards["per_grade"]

    if is_decreasing:
        difference = standard - performance
    else:
        difference = performance - standard

    if difference >= 0:
        score = max_score
    else:
        grades_down = abs(difference) / per_grade
        score_per_grade = standards.get("score_per_grade", 8.75)
        score = max_score - (grades_down * score_per_grade)
        score = max(0, score)

    return score


def page_university_select():
    st.title("체력시험 합격 판정 시스템")
    st.subheader("1단계: 대학교 선택")
    st.write("아래에서 대학교를 선택하여 진행하세요.")

    st.divider()

    params = st.experimental_get_query_params()
    if 'select' in params:
        sel = params.get('select')[0]
        if sel in UNIVERSITY_STANDARDS:
            st.session_state.selected_university = sel
            st.session_state.practical_scores = {}
            st.session_state.naesin_score = 0
            st.session_state.page = "gender_select"
            st.experimental_set_query_params()
            st.rerun()

    col1, col2 = st.columns(2)
    with col1:
        logo_g = DISPLAY_LOGOS.get('가천대학교', '')
        html_g = f"""
<form method='get'>
  <button name='select' value='가천대학교' style='display:flex; align-items:center; gap:12px; width:100%; padding:14px; border-radius:10px; border:1px solid #d0e8d8; background:linear-gradient(180deg,#ffffff,#f6fff7); font-size:16px; cursor:pointer;'>
    <img src='{logo_g}' style='width:56px; height:56px; object-fit:contain;'/>
    <div style='text-align:left;'>
      <div style='font-weight:600;'>가천대학교 체육학부</div>
      <div style='font-size:13px; color:#444;'>내신 300 / 실기 700</div>
    </div>
  </button>
</form>
        """
        st.markdown(html_g, unsafe_allow_html=True)

    with col2:
        logo_s = DISPLAY_LOGOS.get('상명대학교', '')
        html_s = f"""
<form method='get'>
  <button name='select' value='상명대학교' style='display:flex; align-items:center; gap:12px; width:100%; padding:14px; border-radius:10px; border:1px solid #d6e9ff; background:linear-gradient(180deg,#ffffff,#f6faff); font-size:16px; cursor:pointer;'>
    <img src='{logo_s}' style='width:56px; height:56px; object-fit:contain;'/>
    <div style='text-align:left;'>
      <div style='font-weight:600;'>상명대학교 스포츠건강관리</div>
      <div style='font-size:13px; color:#444;'>내신 300 / 실기 700</div>
    </div>
  </button>
</form>
        """
        st.markdown(html_s, unsafe_allow_html=True)


def page_gender_select():
    st.title("체력시험 합격 판정 시스템")
    st.subheader("2단계: 성별 선택")
    st.write("시험을 응시할 성별을 선택하세요. (성별에 따라 기준이 다릅니다)")
    st.divider()
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        selected = st.radio("성별 선택:", ["남자", "여자"], horizontal=True, label_visibility="collapsed")
    st.divider()
    if st.button("다음: 내신점수 입력 ▶", use_container_width=True):
        st.session_state.gender = selected
        st.session_state.page = "naesin_score_input"
        st.rerun()


def page_naesin_score_input():
    st.title("체력시험 합격 판정 시스템")
    st.subheader("3단계: 내신점수 입력")
