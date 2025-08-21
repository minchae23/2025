import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from googleapiclient.discovery import build

# 🔑 API 키 입력
api_key = "YOUR_API_KEY"
youtube = build("youtube", "v3", developerKey=api_key)

st.title("📊 유튜브 채널 분석기")

# 👉 채널 URL 입력
channel_url = st.text_input("채널 URL을 입력하세요 (예: https://www.youtube.com/@혜안)")

def get_channel_stats(username):
    # 채널 정보 가져오기
    request = youtube.channels().list(
        part="snippet,statistics,contentDetails",
        forUsername=username
    )
    response = request.execute()
    return response

if channel_url:
    # 📝 URL에서 채널 ID 또는 username 추출 로직 필요
    channel_data = get_channel_stats("혜안")  # 예시
    
    # 📌 채널 기본 정보 출력
    st.subheader("채널 기본 정보")
    st.write("채널명:", channel_data["items"][0]["snippet"]["title"])
    st.write("구독자 수:", channel_data["items"][0]["statistics"]["subscriberCount"])
    st.write("총 조회수:", channel_data["items"][0]["statistics"]["viewCount"])
    st.write("총 영상 수:", channel_data["items"][0]["statistics"]["videoCount"])

    # 📊 그래프 (예시)
    st.subheader("구독자 성장 그래프 (예시 데이터)")
    st.line_chart([100, 300, 500, 1000, 2000])
