# 1️⃣ 라이브러리 설치 필요
# pip install streamlit google-api-python-client pandas matplotlib plotly wordcloud

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from googleapiclient.discovery import build
from wordcloud import WordCloud

# ===========================
# 2️⃣ API 설정
# ===========================
api_key = "YOUR_API_KEY"  # 여기에 발급받은 YouTube Data API 키 입력
youtube = build("youtube", "v3", developerKey=api_key)

# ===========================
# 3️⃣ Streamlit UI
# ===========================
st.set_page_config(page_title="갸티비 채널 분석기", layout="wide")
st.title("📊 기아타이거즈 공식 유튜브 분석기 (갸티비)")

channel_id = "UCKp8knO8a6tSI1oaLjfd9XA"  # 갸티비 채널 ID

# ===========================
# 4️⃣ 채널 정보 가져오기
# ===========================
def get_channel_stats(channel_id):
    request = youtube.channels().list(
        part="snippet,statistics,contentDetails",
        id=channel_id
    )
    response = request.execute()
    return response

channel_data = get_channel_stats(channel_id)["items"][0]

st.subheader("채널 기본 정보")
st.write("채널명:", channel_data["snippet"]["title"])
st.write("구독자 수:", channel_data["statistics"].get("subscriberCount", "N/A"))
st.write("총 조회수:", channel_data["statistics"].get("viewCount", "N/A"))
st.write("총 영상 수:", channel_data["statistics"].get("videoCount", "N/A"))

# ===========================
# 5️⃣ 영상 리스트 가져오기
# ===========================
def get_video_list(playlist_id, max_results=20):
    videos = []
    request = youtube.playlistItems().list(
        part="snippet",
        playlistId=playlist_id,
        maxResults=max_results
    )
    response = request.execute()
    
    for item in response["items"]:
        video_title = item["snippet"]["title"]
        video_id = item["snippet"]["resourceId"]["videoId"]
        videos.append({"title": video_title, "videoId": video_id})
    return pd.DataFrame(videos)

# 갸티비 채널 업로드 플레이리스트 ID
uploads_playlist_id = channel_data["contentDetails"]["relatedPlaylists"]["uploads"]
video_df = get_video_list(uploads_playlist_id)

st.subheader("최근 영상 목록")
st.dataframe(video_df)

# ===========================
# 6️⃣ 영상 제목 워드클라우드
# ===========================
st.subheader("영상 제목 키워드 워드클라우드")
text = " ".join(video_df["title"])
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)

plt.figure(figsize=(10,5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
st.pyplot(plt)

# ===========================
# 7️⃣ 예시: 구독자 추세 그래프 (더미 데이터)
# ===========================
st.subheader("구독자 성장 추세 (예시)")
# 실제 구독자 추세는 API로 전체 히스토리 데이터를 가져와야 하지만,
# API에서는 기본 제공하지 않아서 예시 데이터로 시각화
import numpy as np
days = np.arange(1, 11)
subs = np.array([1000,1200,1500,1800,2100,2500,3000,3500,4000,4500])  # 예시
plt.figure()
plt.plot(days, subs, marker='o')
plt.title("구독자 수 변화 (예시)")
plt.xlabel("날짜")
plt.ylabel("구독자 수")
st.pyplot(plt)
