# # streamlit_app.py

# 📌 필요한 라이브러리 설치:
# 터미널에서 한 번만 실행
# pip install streamlit pandas plotly

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
    "선수": ["오선우","윤영철","구자욱","강민호","이재원","정우영",
            "박세혁","이재원","전준우","손아섭","양의지","박민우",
            "김하성","이정후","고명준","이로운","정은원","최재훈","강백호","황재균"],
    "타율":[0.312,0.298,0.305,0.280,0.270,0.260,0.290,0.275,0.310,0.295,
           0.305,0.300,0.320,0.310,0.285,0.275,0.265,0.250,0.300,0.295],
    "홈런":[10,8,15,12,9,5,11,7,13,9,14,8,16,12,10,7,6,4,15,11],
    "타점":[45,38,60,50,40,30,48,35,55,42,57,39,62,51,46,33,32,25,58,47],
    "사진":[  # 임시 이미지 URL
        "https://picsum.photos/200/300?1","https://picsum.photos/200/300?2",
        "https://picsum.photos/200/300?3","https://picsum.photos/200/300?4",
        "https://picsum.photos/200/300?5","https://picsum.photos/200/300?6",
        "https://picsum.photos/200/300?7","https://picsum.photos/200/300?8",
        "https://picsum.photos/200/300?9","https://picsum.photos/200/300?10",
        "https://picsum.photos/200/300?11","https://picsum.photos/200/300?12",
        "https://picsum.photos/200/300?13","https://picsum.photos/200/300?14",
        "https://picsum.photos/200/300?15","https://picsum.photos/200/300?16",
        "https://picsum.photos/200/300?17","https://picsum.photos/200/300?18",
        "https://picsum.photos/200/300?19","https://picsum.photos/200/300?20"
    ]
})

# --- 사이드바 메뉴 ---
menu = st.sidebar.radio("메뉴 선택", ["선수 기록 비교", "팀 경기 분석", "나만의 야구 카드", "오늘의 하이라이트"])

# --- 1. 선수 기록 비교 ---
if menu == "선수 기록 비교":
    st.title("선수 기록 비교")
    
    team1 = st.selectbox("첫 번째 구단 선택", teams, key="team1")
    player1 = st.selectbox("첫 번째 선수 선택", players[team1], key="player1")
    
    team2 = st.selectbox("두 번째 구단 선택", teams, key="team2")
    player2 = st.selectbox("두 번째 선수 선택", players[team2], key="player2")
    
    compare_df = player_stats[player_stats['선수'].isin([player1, player2])].reset_index(drop=True)
    st.dataframe(compare_df[['선수','타율','홈런','타점']])
    
    fig = px.bar(compare_df, x='선수', y=['타율','홈런','타점'], barmode='group', title="선수 기록 비교")
    st.plotly_chart(fig)
    
    # 선수 사진
    st.subheader("선수 사진")
    cols = st.columns(2)
    for i, player in enumerate([player1, player2]):
        img_url = player_stats[player_stats['선수']==player]['사진'].values[0]
        cols[i].image(img_url, caption=player, use_column_width=True)

# --- 2. 팀 경기 분석 ---
elif menu == "팀 경기 분석":
    st.title("팀 경기 분석")
    team = st.selectbox("구단 선택", teams, key="team_analysis")
    
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
    team = st.selectbox("구단 선택", teams, key="team_card")
    player = st.selectbox("선수 선택", players[team], key="player_card")
    
    stat = player_stats[player_stats['선수']==player]
    
    st.subheader(f"{player} 카드")
    st.table(stat[['타율','홈런','타점']])
    
    st.image(stat['사진'].values[0], caption=player, use_column_width=True)

# --- 4. 오늘의 하이라이트 ---
elif menu == "오늘의 하이라이트":
    st.title("오늘의 경기 하이라이트")
    team = st.selectbox("구단 선택", teams, key="team_video")
    
    st.write(f"{team} 오늘의 경기 영상")
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")  # 예시 링크
