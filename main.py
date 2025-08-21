import streamlit as st

# ---------------- 페이지 기본 설정 ----------------
st.set_page_config(
    page_title="🌟 MBTI 직업 추천 🎯",
    page_icon="🌈",
    layout="centered"
)

# ---------------- 제목 & 설명 ----------------
st.markdown(
    """
    <h1 style="text-align:center; color:#ff66b2; font-size:60px;">
        🌟 MBTI 기반 진로 추천 🎯
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <h3 style="text-align:center; color:#6a5acd;">
        ✨ 당신의 MBTI를 선택하면,<br> 맞춤형 직업을 추천해드려요! ✨
    </h3>
    """,
    unsafe_allow_html=True
)

st.write("")

# ---------------- MBTI 데이터 ----------------
mbti_jobs = {
    "INTJ": ["🔬 연구원", "📊 전략기획가", "🤖 데이터 분석가"],
    "INTP": ["💻 프로그래머", "🔎 연구개발자", "📚 이론 과학자"],
    "ENTJ": ["💼 CEO", "📈 사업가", "🏢 경영 컨설턴트"],
    "ENTP": ["🚀 기업가", "📺 방송 PD", "🎨 마케팅 기획자"],
    "INFJ": ["💬 심리상담사", "📚 작가", "🎓 교수"],
    "INFP": ["🎶 음악가", "✍️ 시인", "🤝 사회복지사"],
    "ENFJ": ["🎤 강사", "🤝 리더십 코치", "🎓 교육자"],
    "ENFP": ["🎤 크리에이터", "📰 기자", "🎭 광고 기획자"],
    "ISTJ": ["⚖️ 법률가", "📑 회계사", "🪖 군인"],
    "ISFJ": ["🏥 간호사", "🍎 교사", "🏛️ 사회복지사"],
    "ESTJ": ["🏦 금융 전문가", "📋 관리자", "🚔 경찰"],
    "ESFJ": ["👩‍🏫 교사", "👨‍👩‍👧 상담가", "🤲 봉사 단체 활동가"],
    "ISTP": ["🔧 엔지니어", "✈️ 파일럿", "🚘 자동차 정비사"],
    "ISFP": ["🎨 디자이너", "📷 사진작가", "🎶 음악가"],
    "ESTP": ["🏟️ 스포츠 선수", "📣 이벤트 매니저", "💼 세일즈 전문가"],
    "ESFP": ["🎶 가수", "🎬 배우", "🎉 이벤트 플래너"],
}

# ---------------- MBTI 선택 ----------------
st.markdown("### 🧩 MBTI 유형을 선택하세요 🧩")
mbti = st.selectbox("👇 여기서 선택!", list(mbti_jobs.keys()))

st.write("---")

# ---------------- 결과 출력 ----------------
if mbti:
    st.markdown(
        f"""
        <h2 style="color:#ff4500; text-align:center;">
            🌈 ✨ {mbti} 유형을 위한 직업 추천 ✨ 🌈
        </h2>
        """,
        unsafe_allow_html=True
    )

    for job in mbti_jobs[mbti]:
        st.markdown(f"<h3 style='text-align:center;'> {job} </h3>", unsafe_allow_html=True)

    st.balloons()  # 🎈 화려한 풍선 효과
    st.snow()      # ❄️ 눈 효과
