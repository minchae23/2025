import streamlit as st
import requests
import re

# 🔑 여기다가 본인 구글 클라우드에서 발급받은 API KEY 넣어야 함
API_KEY = "YOUR_YOUTUBE_API_KEY"

def extract_channel_id(url):
    """
    유튜브 채널 URL에서 channel_id 추출
    """
    # /channel/ 형태
    match = re.search(r"channel/([A-Za-z0-9_-]+)", url)
    if match:
        return match.group(1)
    return None

def get_channel_stats(channel_id):
    """
    유튜브 Data API v3에서 채널 기본 정보 가져오기
    """
    url = f"https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&id={channel_id}&key={API_KEY}"
    response = requests.get(url).json()

    if "items" not in response or len(response["items"]) == 0:
        return None

    item = response["items"][0]
    data = {
        "채널명": item["snippet"]["title"],
        "설명": item["snippet"]["description"],
        "개설일": item["snippet"]["publishedAt"][:10],
        "구독자 수": item["statistics"].get("subscriberCount", "비공개"),
        "총 조회수": item["statistics"]["viewCount"],
        "영상 개수": item["statistics"]["videoCount"]
    }
    return data

# ----------------- Streamlit UI ----------------- #
st.title("📊 유튜브 채널 기본 정보 분석기")

channel_url = st.text_input("유튜브 채널 URL을 입력하세요:")

if st.button("채널 분석 시작"):
    channel_id = extract_channel_id(channel_url)
    if channel_id:
        data = get_channel_stats(channel_id)
        if data:
            st.subheader("🔎 채널 기본 정보")
            for k, v in data.items():
                st.write(f"**{k}:** {v}")
        else:
            st.error("채널 정보를 가져올 수 없습니다.")
    else:
        st.error("URL에서 채널 ID를 추출할 수 없습니다. /channel/ 형태의 URL을 입력하세요.")

