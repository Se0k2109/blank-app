import streamlit as st
import math

# 페이지 설정
st.set_page_config(page_title="가천대학교 체력시험 합격 판정 시스템", layout="wide")

# 세션 상태 초기화
if 'page' not in st.session_state:
    st.session_state.page = "gender_select"
if 'gender' not in st.session_state:
    st.session_state.gender = None
if 'selected_university' not in st.session_state:
    st.session_state.selected_university = None
if 'converted_score' not in st.session_state:
    st.session_state.converted_score = None
if 'practical_scores' not in st.session_state:
    st.session_state.practical_scores = {
        "배근력검사": None,
        "10m왕복달리기": None,
        "제자리멀리뛰기": None,
        "메디신볼던지기": None
    }

# 가천대학교 기준 정보 (성별별로 구분)
UNIVERSITY_STANDARDS = {
    "가천대학교": {
        "converted_max": 300,
        "practical_max": 700,
        "male": {
                "배근력검사": {
                    "standard": 221,
                    "max_score": 175,
                    "unit": "kg",
                    "decreasing": False,
                    "per_grade": 5
                },
            "10m왕복달리기": {
                "standard": 8.00,
                "max_score": 175,
                "unit": "초",
                "decreasing": True,
                "per_grade": 0.1
            },
            "제자리멀리뛰기": {
                "standard": 300,
                "max_score": 175,
                "unit": "cm",
                "decreasing": False,
                "per_grade": 5
            },
            "메디신볼던지기": {
                "standard": 12.5,
                "max_score": 175,
                "unit": "m",
                "decreasing": False,
                "per_grade": 0.2
            }
        },
        "female": {
                "배근력검사": {
                    "standard": 161,
                    "max_score": 175,
                    "unit": "kg",
                    "decreasing": False,
                    "per_grade": 5
                },
            "10m왕복달리기": {
                "standard": 9.20,
                "max_score": 175,
                "unit": "초",
                "decreasing": True,
                "per_grade": 0.1
            },
            "제자리멀리뛰기": {
                "standard": 240,
                "max_score": 175,
                "unit": "cm",
                "decreasing": False,
                "per_grade": 5
            },
            "메디신볼던지기": {
                "standard": 9.8,
                "max_score": 175,
                "unit": "m",
                "decreasing": False,
                "per_grade": 0.2
            }
        }
    }
}

def calculate_practical_score(event_name, performance, university="가천대학교", gender="남자"):
    """실기 성적에 따른 점수 계산"""
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
        # 1등급감점 = 1감(8.75점)
        grades_down = abs(difference) / per_grade
        score = max_score - (grades_down * 8.75)
        score = max(0, score)
    
    return score

def page_gender_select():
    """1단계: 성별 선택"""
    st.title("🎫 체력시험 합격 판정 시스템")
    st.subheader("1단계: 성별 선택")
    
    st.write("시험을 응시할 성별을 선택하세요. (성별에 따라 기준이 다릅니다)")
    st.divider()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        selected = st.radio(
            "성별 선택:",
            ["남자", "여자"],
            horizontal=True,
            label_visibility="collapsed"
        )
    
    st.divider()
    
    if st.button("다음: 대학교 선택 ▶", use_container_width=True):
        st.session_state.gender = selected
        st.session_state.page = "university_select"
        st.rerun()

def page_university_select():
    """2단계: 대학교 선택"""
    st.title("🏫 체력시험 합격 판정 시스템")
    st.subheader("2단계: 대학교 선택")
    
    st.write("아래에서 대학교를 선택하여 진행하세요.")
    st.divider()
    
    # 카드형 대학교 선택 UI
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # 가천대학교 카드
        with st.container(border=True):
            st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
            st.markdown("## 🏫 가천대학교")
            st.markdown("**Gachon University**", unsafe_allow_html=True)
            st.markdown("---")
            st.caption("체력시험 합격 판정 시스템")
            st.markdown("</div>", unsafe_allow_html=True)
            
            if st.button("✅ 가천대학교 선택", use_container_width=True, key="gachon_select"):
                st.session_state.selected_university = "가천대학교"
                st.session_state.page = "converted_score_input"
                st.rerun()

def page_converted_score_input():
    """3단계: 환산점수 입력"""
    st.title("🏫 체력시험 합격 판정 시스템")
    st.subheader("3단계: 환산점수 입력")
    
    university = st.session_state.selected_university
    max_converted = UNIVERSITY_STANDARDS[university]["converted_max"]
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("선택된 대학교", university)
    with col2:
        st.metric("환산점수 만점", f"{max_converted}점")
    
    st.write("**기준은 만점 기준입니다.**")
    st.divider()
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        converted_score = st.number_input(
            f"환산점수를 입력하세요:",
            value=0,
            step=1,
            key="converted_input"
        )
    
    with col2:
        st.metric("입력된 환산점수", f"{converted_score}점")
    
    st.divider()
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("◀ 이전 단계로", use_container_width=True):
            st.session_state.page = "university_select"
            st.rerun()
    
    with col2:
        if st.button("다음: 성적입력 ▶", use_container_width=True):
            st.session_state.converted_score = converted_score
            st.session_state.page = "practical_score_input"
            st.rerun()

def page_practical_score_input():
    """4단계: 실기 점수 입력"""
    st.title("🏫 체력시험 합격 판정 시스템")
    st.subheader("4단계: 실기 종목별 성적 입력")
    
    university = st.session_state.selected_university
    gender = st.session_state.gender
    converted_score = st.session_state.converted_score
    gender_key = "male" if gender == "남자" else "female"
    events = UNIVERSITY_STANDARDS[university][gender_key]
    
    # 상단 정보 표시
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("대학교", university)
    with col2:
        st.metric("성별", gender)
    with col3:
        st.metric("환산점수", f"{converted_score}점")
    
    st.divider()
    st.write("**📌 입력 기준:** 만점 기준이며, 1등급감점 = 1감(8.75점) 입니다.")
    st.divider()
    
    # 깔끔한 테이블 형식으로 입력칸 정리
    st.write("#### 📊 실기 종목 성적 입력")
    
    # 테이블 헤더
    col_header1, col_header2, col_header3, col_header4 = st.columns([2.5, 1.5, 1, 1.5])
    with col_header1:
        st.write("**종목명**")
    with col_header2:
        st.write("**기준(만점)**")
    with col_header3:
        st.write("**단위**")
    with col_header4:
        st.write("**성적입력**")
    
    st.divider()
    
    # 각 종목별 입력
    for idx, (event_name, standards) in enumerate(events.items()):
        col1, col2, col3, col4 = st.columns([2.5, 1.5, 1, 1.5])
        
        with col1:
            st.write(f"**{event_name}**")
        
        with col2:
            st.write(f"{standards['standard']}")
        
        with col3:
            st.write(f"{standards['unit']}")
        
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
            st.session_state.page = "converted_score_input"
            st.rerun()
    
    with col2:
        if st.button("다음: 최종 결과 보기 ▶", use_container_width=True):
            st.session_state.page = "result"
            st.rerun()

def page_result():
    """4단계: 최종 결과"""
    st.title("🏫 체력시험 합격 판정 시스템")
    st.subheader("4단계: 최종 결과")
    
    university = st.session_state.selected_university
    gender = st.session_state.gender
    converted_score = st.session_state.converted_score
    practical_scores = st.session_state.practical_scores
    gender_key = "male" if gender == "남자" else "female"
    events = UNIVERSITY_STANDARDS[university][gender_key]
    
    # 상단 정보 표시
    col1, col2 = st.columns(2)
    with col1:
        st.metric("선택된 대학교", university)
    with col2:
        st.metric("성별", gender)
    st.divider()
    
    st.write("### 📊 환산점수")
    st.metric("환산점수", f"{converted_score}점 / {UNIVERSITY_STANDARDS[university]['converted_max']}점")
    
    st.divider()
    
    st.write("### 🏃 실기 성적 및 점수")
    
    total_practical_score = 0
    practical_details = []
    
    for event_name, performance in practical_scores.items():
        perf_val = performance if (performance is not None) else 0.0
        score = calculate_practical_score(event_name, perf_val, university, gender)
        total_practical_score += score
        
        standards = events[event_name]
        practical_details.append({
            "종목": event_name,
            "성적": (f"{performance}{standards['unit']}" if performance is not None else "미입력"),
            "획득점수": f"{score:.2f}점"
        })
    
    # 테이블 형식으로 실기 성적 표시
    col_h1, col_h2, col_h3 = st.columns([2, 1.5, 1.5])
    with col_h1:
        st.write("**종목명**")
    with col_h2:
        st.write("**성적**")
    with col_h3:
        st.write("**획득점수**")
    st.divider()
    
    for detail in practical_details:
        col1, col2, col3 = st.columns([2, 1.5, 1.5])
        with col1:
            st.write(detail['종목'])
        with col2:
            st.write(detail['성적'])
        with col3:
            st.write(detail['획득점수'])
    
    st.divider()
    st.metric("실기 총점", f"{total_practical_score:.2f}점 / {UNIVERSITY_STANDARDS[university]['practical_max']}점")
    
    st.divider()
    
    st.write("### 📋 최종 결과")
    total_score = converted_score + total_practical_score
    max_total_score = UNIVERSITY_STANDARDS[university]["converted_max"] + UNIVERSITY_STANDARDS[university]["practical_max"]
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.metric("환산점수", f"{converted_score}점")
    with col2:
        st.metric("실기총점", f"{total_practical_score:.2f}점")
    with col3:
        st.metric("합계", f"{total_score:.2f}점")
    
    st.divider()
    
    st.write("### ✅ 합격 판정")
    
    # 사용자 요청에 따른 합격 범주 표시 (시각적으로 정리)
    st.markdown("---")
    st.subheader("🔎 예상 지원 권장 안내")
    st.write("**선택된 판정 기준 (총점 최대 1000점 기준)**")
    st.write("- 900점 이상: 합격유력으로 지원가능")
    st.write("- 895점 이상: 합격긍정으로 소신지원가능")
    st.write("- 894점 이하: 합격이 어려워 지원불가")

    # 주요 판정 배지
    if total_score >= 900:
        st.success("🎉 합격유력으로 지원가능", icon="✅")
    elif total_score >= 895:
        st.info("👍 합격긍정으로 소신지원가능")
    else:
        st.error("🚫 지원불가: 합격이 어려움", icon="❌")

    st.write(f"**현재 획득점수:** {total_score:.2f}점")

    # 부족점수 및 '감' 계산 (사용자 요청: 8.5로 나누어 감 계산)
    st.markdown("---")
    st.subheader("📌 부족 점수와 필요 등급(감) 계산")
    st.caption("계산 기준: 1감 = 8.5점 (예상용), 기준은 만점 기준을 기준으로 합니다.")

    cutoffs = [900, 895]
    for cutoff in cutoffs:
        diff = round(max(0.0, cutoff - total_score), 2)
        if diff <= 0:
            col_a, col_b = st.columns([3, 2])
            with col_a:
                st.markdown(f"**{cutoff}점 컷충족 상태**")
            with col_b:
                st.metric(f"컷 {cutoff}", "충족", delta=f"{diff:.2f}점")
        else:
            needed_gam = math.ceil(diff / 8.5)
            col1, col2, col3 = st.columns([2, 2, 2])
            with col1:
                st.write(f"**컷 {cutoff}점까지 부족:**")
                st.write(f"- 부족 점수: **{diff:.2f}점**")
            with col2:
                st.write(f"**필요한 감(등급)**")
                st.write(f"- 약 **{diff/8.5:.2f}감** (정수로는 **{needed_gam}감** 필요)")
            with col3:
                st.metric(f"{cutoff} 컷까지", f"{diff:.2f}점 부족", delta=f"{needed_gam}감 필요")

    st.markdown("---")
    
    st.divider()
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("◀ 이전 단계로", use_container_width=True):
            st.session_state.page = "practical_score_input"
            st.rerun()
    
    with col2:
        if st.button("🔄 처음부터 다시 시작", use_container_width=True):
            st.session_state.page = "gender_select"
            st.session_state.gender = None
            st.session_state.selected_university = None
            st.session_state.converted_score = None
            st.session_state.practical_scores = {
                "배근력검사": None,
                "10m왕복달리기": None,
                "제자리멀리뛰기": None,
                "메디신볼던지기": None
            }
            st.rerun()

# 페이지 라우팅
if st.session_state.page == "gender_select":
    page_gender_select()
elif st.session_state.page == "university_select":
    page_university_select()
elif st.session_state.page == "converted_score_input":
    page_converted_score_input()
elif st.session_state.page == "practical_score_input":
    page_practical_score_input()
elif st.session_state.page == "result":
    page_result()
