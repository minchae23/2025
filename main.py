import streamlit as st

# MBTI별 직업 추천 데이터
mbti_jobs = {
    "INTJ": ["연구원", "전략기획가", "데이터 분석가"],
    "ENTP": ["기업가", "마케팅 기획자", "방송 PD"],
    "INFJ": ["심리상담사", "작가", "교수"],
    "ENFP": ["광고기획자", "기자", "크리에이터"],
    "ISTJ": ["회계사", "법률가", "군인"],
    "ESFP": ["배우", "디자이너", "이벤트 플래너"],
    # 필요에 따라 추가 가능
}

st.set_page_config(page_title="MBTI 직업 추천", page_icon="🎯", layout="centered")

st.title("🎯 MBTI 기반 진로 추천")
st.write("당신의 MBTI를 선택하면, 적합한 직업을 추천해드려요!")

# 사용자 입력
mbti = st.selectbox("MBTI 유형을 선택하세요:", list(mbti_jobs.keys()))

if mbti:
    st.subheader(f"✨ {mbti} 유형에게 추천하는 직업")
    for job in mbti_jobs[mbti]:
        st.markdown(f"- {job}")

