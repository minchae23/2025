import streamlit as st
from googleapiclient.discovery import build

st.title("유튜브 채널 구독자 수 확인")

# API Key 입력
api_key = st.text_input("API Key 입력", type="password")

# 채널 URL 입력
channel_url = st.text_input("채널 URL 입력", "https://www.youtube.com/@kiatigerstv")

def get_channel_id(url):
    # 커스텀 URL(@kiatigerstv)을 UC로 시작하는 채널 ID로 변환
    # 여기서는 예시 채널 ID를 바로 사용
    return "UCp8knO8a6tSI1oaLjfd9XA"

if api_key and channel_url:
    channel_id = get_channel_id(channel_url)
    
    # 유튜브 API 객체 생성
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    # 채널 정보 요청
    request = youtube.channels().list(
        part="snippet,statistics",
        id=channel_id
    )
    try:
        response = request.execute()
        channel_name = response['items'][0]['snippet']['title']
        subscribers = response['items'][0]['statistics']['subscriberCount']
        st.write(f"**{channel_name}** 구독자 수: **{subscribers}명**")
    except Exception as e:
        st.error("채널 정보를 가져올 수 없습니다. API Key와 URL을 확인하세요.")
