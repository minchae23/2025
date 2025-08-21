import streamlit as st
import pandas as pd
import plotly.express as px

# --- 예시 데이터 ---
teams = ["기아", "삼성", "LG", "두산", "롯데", "NC", "키움", "SSG", "한화", "KT"]
players = {
    "기아": ["오선우", "윤영철"],
    "삼성": ["구자욱", "강민호"],
    "LG": ["이재원", "정우영"],
    "두산": ["박세혁", "이재원"],
    "롯데": ["전준우", "손아섭"],
    "NC": ["양의지", "박민우"],
    "키움": ["김하성", "이정후"],
    "SSG": ["고명준", "이로운"],
    "한화": ["정은원", "최재훈"],
    "KT": ["강백호", "황재균"]
}

player_stats = pd.DataFrame({
    "선수": ["오선우","고명준","구자욱","강민호","이재원","정우영"],
    "타율":[0.312,0.298,0.305,0.280,0.270,0.260],
    "홈런":[10,8,15,12,9,5],
    "타점":[45,38,60,50,40,30]
})

# --- 사이드바 메뉴 ---
menu = st.sidebar.radio("메뉴 선택", ["선수 기록 비교", "팀 경기 분석", "나만의 야구 카드", "오늘의 하이라이트"])

# --- 1. 선수 기록 비교 ---
if menu == "선수 기록 비교":
    st.title("선수 기록 비교")
    
    team1 = st.selectbox("첫 번째 구단 선택", teams)
    player1 = st.selectbox("첫 번째 선수 선택", players[team1])
    
    team2 = st.selectbox("두 번째 구단 선택", teams)
    player2 = st.selectbox("두 번째 선수 선택", players[team2])
    
    compare_df = player_stats[player_stats['선수'].isin([player1, player2])]
    
    st.dataframe(compare_df)
    
    fig = px.bar(compare_df, x='선수', y=['타율','홈런','타점'], barmode='group', title="선수 기록 비교")
    st.plotly_chart(fig)

# --- 2. 팀 경기 분석 ---
elif menu == "팀 경기 분석":
    st.title("팀 경기 분석")
    team = st.selectbox("구단 선택", teams)
    
    # 예시 경기 기록 데이터
    games = pd.DataFrame({
        "경기": ["1","2","3","4","5"],
        "득점": [3,5,2,6,4],
        "실점": [2,4,3,1,5]
    })
    
    st.write(f"{team} 최근 5경기 기록")
    st.dataframe(games)
    
    fig = px.line(games, x="경기", y=["득점","실점"], markers=True, title=f"{team} 득점/실점 추이")
    st.plotly_chart(fig)

# --- 3. 나만의 야구 카드 ---
elif menu == "나만의 야구 카드":
    st.title("나만의 야구 카드 만들기")
    team = st.selectbox("구단 선택", teams)
    player = st.selectbox("선수 선택", players[team])
    
    st.subheader(f"{player} 카드")
    st.write("타율, 홈런, 타점 확인")
    stat = player_stats[player_stats['선수']==player]
    st.table(stat)
    
    st.image("https://picsum.photos/200/300")  # 예시 이미지

# --- 4. 오늘의 하이라이트 ---
elif menu == "오늘의 하이라이트":
    st.title("오늘의 경기 하이라이트")
    team = st.selectbox("구단 선택", teams)
    
    st.write(f"{team} 오늘의 경기 영상")
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")  # 예시 링크
