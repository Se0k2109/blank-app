import streamlit as st

# 페이지 설정
st.set_page_config(page_title="가천대학교 체력시험 합격 판정 시스템", layout="wide")

# 세션 상태 초기화
if 'page' not in st.session_state:
    st.session_state.page = "university_select"
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

# 가천대학교 기준 정보
UNIVERSITY_STANDARDS = {
    "가천대학교": {
        "converted_max": 300,
        "practical_max": 700,
        "events": {
            "배근력검사": {
                "standard": 221,
                "max_score": 175,
                "unit": "kg",
                "decreasing": True,
                "per_grade": 4
            },
            "10m왕복달리기": {
                "standard": 8.0,
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
        }
    }
}

def calculate_practical_score(event_name, performance, university="가천대학교"):
    """실기 성적에 따른 점수 계산"""
    standards = UNIVERSITY_STANDARDS[university]["events"][event_name]
    
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
        score = max_score - (grades_down * (max_score / 8.75))
        score = max(0, score)
    
    return score

def page_university_select():
    """1단계: 대학교 선택"""
    st.title("🏫 체력시험 합격 판정 시스템")
    st.subheader("1단계: 대학교 선택")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.info("현재 가천대학교만 지원합니다.")
    
    with col2:
        selected = st.selectbox(
            "대학교를 선택하세요:",
            list(UNIVERSITY_STANDARDS.keys()),
            key="university_select"
        )
    
    if st.button("다음 단계로 진행 →"):
        st.session_state.selected_university = selected
        st.session_state.page = "converted_score_input"
        st.rerun()

def page_converted_score_input():
    """2단계: 환산점수 입력"""
    st.title("🏫 체력시험 합격 판정 시스템")
    st.subheader("2단계: 환산점수 입력")
    
    university = st.session_state.selected_university
    max_converted = UNIVERSITY_STANDARDS[university]["converted_max"]
    
    st.write(f"**선택된 대학교:** {university}")
    st.write(f"**환산점수 만점:** {max_converted}점")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        converted_score = st.number_input(
            f"환산점수를 입력하세요 (0~{max_converted}점):",
            min_value=0,
            max_value=max_converted,
            value=0,
            step=1
        )
    
    with col2:
        st.metric("입력된 환산점수", f"{converted_score}점")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("이전 단계로 ←"):
            st.session_state.page = "university_select"
            st.rerun()
    
    with col2:
        if st.button("다음 단계로 진행 →"):
            st.session_state.converted_score = converted_score
            st.session_state.page = "practical_score_input"
            st.rerun()

def page_practical_score_input():
    """3단계: 실기 점수 입력"""
    st.title("🏫 체력시험 합격 판정 시스템")
    st.subheader("3단계: 실기 종목별 성적 입력")
    
    university = st.session_state.selected_university
    converted_score = st.session_state.converted_score
    events = UNIVERSITY_STANDARDS[university]["events"]
    
    st.write(f"**선택된 대학교:** {university}")
    st.write(f"**환산점수:** {converted_score}점")
    st.divider()
    
    for event_name, standards in events.items():
        st.write(f"### {event_name}")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            st.write(f"**기준:** {standards['standard']} {standards['unit']}")
        
        with col2:
            st.write(f"**만점:** {standards['max_score']}점")
        
        with col3:
            if standards['decreasing']:
                st.write(f"**감점 기준:** {standards['per_grade']}{standards['unit']}당 1등급")
            else:
                st.write(f"**감점 기준:** {standards['per_grade']}{standards['unit']}당 1등급")
        
        performance = st.number_input(
            f"{event_name} 성적 입력 ({standards['unit']}):",
            min_value=0.0,
            value=float(st.session_state.practical_scores[event_name]) if st.session_state.practical_scores[event_name] is not None else 0.0,
            step=0.1,
            key=f"input_{event_name}"
        )
        
        st.session_state.practical_scores[event_name] = performance
        st.divider()
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("이전 단계로 ←"):
            st.session_state.page = "converted_score_input"
            st.rerun()
    
    with col2:
        if st.button("최종 결과 보기 →"):
            st.session_state.page = "result"
            st.rerun()

def page_result():
    """4단계: 최종 결과"""
    st.title("🏫 체력시험 합격 판정 시스템")
    st.subheader("4단계: 최종 결과")
    
    university = st.session_state.selected_university
    converted_score = st.session_state.converted_score
    practical_scores = st.session_state.practical_scores
    events = UNIVERSITY_STANDARDS[university]["events"]
    
    st.write(f"**선택된 대학교:** {university}")
    st.divider()
    
    st.write("### 📊 환산점수")
    st.metric("환산점수", f"{converted_score}점 / {UNIVERSITY_STANDARDS[university]['converted_max']}점")
    
    st.divider()
    
    st.write("### 🏃 실기 성적 및 점수")
    
    total_practical_score = 0
    practical_details = []
    
    for event_name, performance in practical_scores.items():
        score = calculate_practical_score(event_name, performance, university)
        total_practical_score += score
        
        standards = events[event_name]
        practical_details.append({
            "종목": event_name,
            "성적": f"{performance}{standards['unit']}",
            "획득점수": f"{score:.2f}점"
        })
    
    for detail in practical_details:
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.write(f"**{detail['종목']}**")
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
    
    passing_score = max_total_score * 0.6
    
    if total_score >= passing_score:
        st.success(f"🎉 **합격** 입니다!", icon="✅")
        st.write(f"획득점수: **{total_score:.2f}점** (합격선: {passing_score:.2f}점 이상)")
    else:
        st.error(f"😢 **불합격** 입니다.", icon="❌")
        st.write(f"획득점수: **{total_score:.2f}점** (합격선: {passing_score:.2f}점 이상)")
        st.write(f"필요한 추가점수: **{passing_score - total_score:.2f}점**")
    
    st.divider()
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("이전 단계로 ←"):
            st.session_state.page = "practical_score_input"
            st.rerun()
    
    with col2:
        if st.button("처음부터 다시 시작 🔄"):
            st.session_state.page = "university_select"
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
if st.session_state.page == "university_select":
    page_university_select()
elif st.session_state.page == "converted_score_input":
    page_converted_score_input()
elif st.session_state.page == "practical_score_input":
    page_practical_score_input()
elif st.session_state.page == "result":
    page_result()
