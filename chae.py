import streamlit as st
from googleapiclient.discovery import build

st.set_page_config(page_title="유튜브 채널 확인", page_icon="📺")

st.title("유튜브 채널 구독자 수 확인")
st.write("채널 URL이 아닌 **채널 ID(UC로 시작하는 ID)** 를 입력해주세요.")

# 1️⃣ API Key 입력
api_key = st.text_input("API Key 입력", type="password")

# 2️⃣ 채널 ID 입력
channel_id = st.text_input("채널 ID 입력", "UCp8knO8a6tSI1oaLjfd9XA")

if api_key and channel_id:
    try:
        # 유튜브 API 객체 생성
        youtube = build('youtube', 'v3', developerKey=api_key)

        # 채널 정보 요청
        request = youtube.channels().list(
            part="snippet,statistics",
            id=channel_id
        )
        response = request.execute()

        # 채널 이름, 구독자 수, Description 가져오기
        channel_name = response['items'][0]['snippet']['title']
        subscribers = response['items'][0]['statistics']['subscriberCount']
        description = response['items'][0]['snippet']['description']

        # 화면에 표시
        st.subheader("채널 정보")
        st.write(f"**채널 이름:** {channel_name}")
        st.write(f"**구독자 수:** {subscribers}명")
        st.write(f"**채널 설명:** {description}")

    except Exception as e:
        st.error("채널 정보를 가져올 수 없습니다. API Key와 채널 ID를 확인하세요.")
