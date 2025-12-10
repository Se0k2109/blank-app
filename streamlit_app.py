import streamlit as st
import math

st.set_page_config(page_title="체력시험 합격 판정 시스템", layout="wide")

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

UNIVERSITY_STANDARDS = {
    "가천대학교": {
        "naesin_max": 300,
        "practical_max": 700,
        "pass_excellent": 900,
        "pass_good": 895,
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
        "pass_excellent": 940,
        "pass_good": 935,
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
    col1, col2 = st.columns(2)
    with col1:
        logo_g = DISPLAY_LOGOS.get('가천대학교', '')
        col_img, col_text = st.columns([0.3, 0.7])
        with col_img:
            st.image(logo_g, width=56)
        with col_text:
            st.write("**가천대학교 체육학부**")
            st.write("<small>내신 300 / 실기 700</small>", unsafe_allow_html=True)
        if st.button("선택", key="btn_gacheon", use_container_width=True):
            st.session_state.selected_university = "가천대학교"
            st.session_state.practical_scores = {}
            st.session_state.naesin_score = 0
            st.session_state.page = "gender_select"
            st.rerun()
    with col2:
        logo_s = DISPLAY_LOGOS.get('상명대학교', '')
        col_img, col_text = st.columns([0.3, 0.7])
        with col_img:
            st.image(logo_s, width=56)
        with col_text:
            st.write("**상명대학교 스포츠건강관리**")
            st.write("<small>내신 300 / 실기 700</small>", unsafe_allow_html=True)
        if st.button("선택", key="btn_sangmyung", use_container_width=True):
            st.session_state.selected_university = "상명대학교"
            st.session_state.practical_scores = {}
            st.session_state.naesin_score = 0
            st.session_state.page = "gender_select"
            st.rerun()

def page_gender_select():
    st.title("체력시험 합격 판정 시스템")
    st.subheader("2단계: 성별 선택")
    st.write("시험을 응시할 성별을 선택하세요. (성별에 따라 기준이 다릅니다)")
    selected = st.radio("성별 선택:", ["남자", "여자"], horizontal=True)
    st.divider()
    if st.button("다음: 내신점수 입력 ▶", use_container_width=True):
        st.session_state.gender = selected
        st.session_state.page = "naesin_score_input"
        st.rerun()

def page_naesin_score_input():
    st.title("체력시험 합격 판정 시스템")
    st.subheader("3단계: 내신점수 입력")
    university = st.session_state.selected_university
    max_naesin = UNIVERSITY_STANDARDS[university]["naesin_max"]
    display_uni = DISPLAY_NAMES.get(university, university)
    col1, col2 = st.columns(2)
    with col1:
        st.metric("선택된 대학교", display_uni)
    with col2:
        st.metric("내신점수 만점", f"{max_naesin}점")
    st.write("**기준은 만점 기준입니다.**")
    st.divider()
    col1, col2 = st.columns([1, 1])
    with col1:
        naesin_score = st.number_input("내신점수를 입력하세요:", value=0, step=1, key="naesin_input")
    with col2:
        st.metric("입력된 내신점수", f"{naesin_score}점")
    st.divider()
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("◀ 이전 단계로", use_container_width=True):
            st.session_state.page = "university_select"
            st.rerun()
    with col2:
        if st.button("다음: 실기 성적입력 ▶", use_container_width=True):
            st.session_state.naesin_score = naesin_score
            st.session_state.page = "practical_score_input"
            st.rerun()

def page_practical_score_input():
    st.title("체력시험 합격 판정 시스템")
    st.subheader("4단계: 실기 종목별 성적 입력")
    university = st.session_state.selected_university
    gender = st.session_state.gender
    naesin_score = st.session_state.naesin_score
    gender_key = "male" if gender == "남자" else "female"
    events = UNIVERSITY_STANDARDS[university][gender_key]
    for event_name in events.keys():
        if event_name not in st.session_state.practical_scores:
            st.session_state.practical_scores[event_name] = None
    display_uni = DISPLAY_NAMES.get(university, university)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("대학교", display_uni)
    with col2:
        st.metric("성별", gender)
    with col3:
        st.metric("내신점수", f"{naesin_score}점")
    st.divider()
    st.write("**📌 입력 기준:** 기준은 만점 기준이며, 각 종목의 1등급당 점수는 표에서 확인하세요.")
    st.divider()
    st.write("#### 📊 실기 종목 성적 입력")
    col_header1, col_header2, col_header3, col_header4 = st.columns([2.5, 2, 2, 1.3])
    with col_header1:
        st.write("**종목명**")
    with col_header2:
        st.write("**기준(만점)**")
    with col_header3:
        st.write("**급간당 점수**")
    with col_header4:
        st.write("**성적입력**")
    st.divider()
    for idx, (event_name, standards) in enumerate(events.items()):
        col1, col2, col3, col4 = st.columns([2.5, 2, 2, 1.3])
        with col1:
            st.write(f"**{event_name}**")
        with col2:
            st.write(f"{standards['standard']}{standards['unit']}")
        with col3:
            score_per_grade = standards.get('score_per_grade', 8.75)
            unit_per_grade = standards.get('per_grade')
            st.write(f"{score_per_grade}점 / {unit_per_grade}{standards['unit']}")
        with col4:
            performance = st.number_input(
                f"성적 입력",
                value=float(st.session_state.practical_scores[event_name]) if st.session_state.practical_scores[event_name] is not None else 0.0,
                step=0.1,
                key=f"input_{event_name}",
                label_visibility="collapsed"
            )
            st.session_state.practical_scores[event_name] = performance
    st.divider()
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("◀ 이전 단계로", use_container_width=True):
            st.session_state.page = "naesin_score_input"
            st.rerun()
    with col2:
        if st.button("다음: 최종 결과 보기 ▶", use_container_width=True):
            st.session_state.page = "result"
            st.rerun()

def page_result():
    st.title("🏫 체력시험 합격 판정 결과")
    st.subheader("4단계: 최종 결과")
    university = st.session_state.selected_university
    gender = st.session_state.gender
    naesin_score = st.session_state.get('naesin_score', 0)
    practical_scores = st.session_state.practical_scores
    gender_key = "male" if gender == "남자" else "female"
    events = UNIVERSITY_STANDARDS[university][gender_key]
    total_practical_score = 0
    practical_rows = []
    for event_name, perf in practical_scores.items():
        perf_val = perf if (perf is not None) else 0.0
        score = calculate_practical_score(event_name, perf_val, university, gender)
        total_practical_score += score
        practical_rows.append({"종목": event_name, "실기 기록": perf if perf is not None else "미입력", "획득점수": round(score, 2)})
    total_score = naesin_score + total_practical_score
    naesin_max = UNIVERSITY_STANDARDS[university]["naesin_max"]
    practical_max = UNIVERSITY_STANDARDS[university]["practical_max"]
    max_total = naesin_max + practical_max
    m1, m2, m3, m4 = st.columns([2, 2, 2, 2])
    with m1:
        st.metric("대학교", DISPLAY_NAMES.get(university, university))
    with m2:
        st.metric("내신점수", f"{naesin_score} / {naesin_max}")
    with m3:
        st.metric("실기총점", f"{total_practical_score:.2f} / {practical_max}")
    with m4:
        st.metric("합계", f"{total_score:.2f} / {max_total}")
    st.divider()
    pass_excellent = UNIVERSITY_STANDARDS[university].get("pass_excellent", 900)
    pass_good = UNIVERSITY_STANDARDS[university].get("pass_good", 895)
    if total_score >= pass_excellent:
        st.success(f"🎉 합격유력 ({pass_excellent}점 이상)")
    elif total_score >= pass_good:
        st.info(f"👍 합격긍정 ({pass_good}~{pass_excellent-1}점)")
    else:
        st.error(f"🚫 불합격권 ({pass_good-1}점 이하)")
    with st.expander("세부 항목 보기 (실기 종목별 점수)"):
        if practical_rows:
            import pandas as pd
            df = pd.DataFrame(practical_rows)
            df = df[["종목", "실기 기록", "획득점수"]]
            st.table(df)
        else:
            st.write("실기 입력 값이 없습니다.")
    st.divider()
    c1, c2 = st.columns([1, 1])
    with c1:
        if st.button("◀ 이전 단계로", use_container_width=True):
            st.session_state.page = "practical_score_input"
            st.rerun()
    with c2:
        if st.button("🔄 처음부터 다시 시작", use_container_width=True):
            st.session_state.page = "university_select"
            st.session_state.gender = None
            st.session_state.selected_university = None
            st.session_state.naesin_score = None
            st.session_state.practical_scores = {}
            st.rerun()

if st.session_state.page == "university_select":
    page_university_select()
elif st.session_state.page == "gender_select":
    page_gender_select()
elif st.session_state.page == "naesin_score_input":
    page_naesin_score_input()
elif st.session_state.page == "practical_score_input":
    page_practical_score_input()
elif st.session_state.page == "result":
    page_result()
