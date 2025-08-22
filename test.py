import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

# 🔑 본인의 YouTube Data API Key 입력
API_KEY = "YOUR_YOUTUBE_API_KEY"

# ----------------- 채널 ID 추출 ----------------- #
def get_channel_id_from_url(url):
    """
    /channel/ 또는 /@username URL 모두 처리
    """
    # /channel/ URL
    if "/channel/" in url:
        return url.split("/channel/")[1].split("?")[0]
    # /@username URL
    elif "/@" in url:
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers)
            html = response.text
            # HTML에서 channelId 찾기
            match = re.search(r'"channelId":"(UC[0-9A-Za-z_-]{22})"', html)
            if match:
                return match.group(1)
        except:
            return None
    return None

# ----------------- 채널 기본 정보 ----------------- #
def get_channel_stats(channel_id):
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

# ----------------- 키워드 영상 검색 ----------------- #
def search_videos_by_keyword(channel_id, keyword, max_results=10):
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={channel_id}&q={keyword}&type=video&maxResults={max_results}&key={API_KEY}"
    response = requests.get(url).json()
    videos = []
    if "items" in response:
        for item in response["items"]:
            video_data = {
                "제목": item["snippet"]["title"],
                "영상 URL": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                "게시일": item["snippet"]["publishedAt"][:10],
                "썸네일": item["snippet"]["thumbnails"]["medium"]["url"]
            }
            videos.append(video_data)
    return videos

# ----------------- Streamlit UI ----------------- #
st.title("📊 유튜브 채널 분석기 & 키워드 영상 검색기")

st.info(
    "⚠️ URL만 입력하면 자동으로 채널 ID를 찾아 분석합니다.\n"
    "예: https://www.youtube.com/@kiatigerstv 또는 https://www.youtube.com/channel/UCxxxx..."
)

channel_url = st.text_input("유튜브 채널 URL을 입력하세요:")

if st.button("채널 분석 시작"):
    if not channel_url:
        st.error("URL을 입력해주세요.")
    else:
        channel_id = get_channel_id_from_url(channel_url)
        if channel_id:
            data = get_channel_stats(channel_id)
            if data:
                st.subheader("🔎 채널 기본 정보")
                for k, v in data.items():
                    st.write(f"**{k}:** {v}")

                # 키워드 검색
                keyword = st.text_input("검색할 키워드를 입력하세요:")
                if keyword:
                    videos = search_videos_by_keyword(channel_id, keyword)
                    if videos:
                        st.subheader(f"🎬 '{keyword}' 관련 영상 리스트")
                        for video in videos:
                            st.write(f"**제목:** {video['제목']}")
                            st.write(f"**게시일:** {video['게시일']}")
                            st.write(f"[영상 링크]({video['영상 URL']})")
                            st.image(video['썸네일'])
                    else:
                        st.info("해당 키워드 관련 영상이 없습니다.")
            else:
                st.error("채널 정보를 가져올 수 없습니다. API Key 또는 URL을 확인해주세요.")
        else:
            st.error("채널 ID를 추출할 수 없습니다. URL을 다시 확인해주세요.")
