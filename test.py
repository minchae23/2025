import streamlit as st
import requests

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(layout="wide", page_title="YouTube Info Viewer", page_icon="▶")

# ✅ 고정 API 키 (수정 금지)
API_KEY = "AIzaSyCaL-ueb_PHj8j_4WgAol4thJMcwQF55Vc"

# -----------------------------
# 채널 정보 가져오기
# -----------------------------
def get_channel_info(channel_id):
    url = f"https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&id={channel_id}&key={API_KEY}"
    response = requests.get(url).json()

    if "items" not in response or len(response["items"]) == 0:
        return None

    data = response["items"][0]
    snippet = data["snippet"]
    stats = data["statistics"]

    return {
        "title": snippet["title"],
        "description": snippet.get("description", ""),
        "thumbnail": snippet["thumbnails"]["high"]["url"],
        "subscribers": stats.get("subscriberCount", "0"),
        "videos": stats.get("videoCount", "0"),
        "views": stats.get("viewCount", "0")
    }

# -----------------------------
# 키워드로 영상 검색
# -----------------------------
def search_videos(query, max_results=6):
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&q={query}&maxResults={max_results}&key={API_KEY}"
    response = requests.get(url).json()

    videos = []
    if "items" in response:
        for item in response["items"]:
            videos.append({
                "title": item["snippet"]["title"],
                "thumbnail": item["snippet"]["thumbnails"]["high"]["url"],
                "videoId": item["id"]["videoId"]
            })
    return videos

# -----------------------------
# UI - 유튜브 스타일 레이아웃
# -----------------------------

# 🔴 상단 (로고 + 안내 문구)
st.markdown("""
    <div style="display:flex; align-items:center; justify-content:space-between; padding:10px; border-bottom:1px solid #ddd;">
        <div style="font-size:24px; font-weight:bold; color:red;">▶ YouTube</div>
        <div style="font-size:18px; font-weight:bold;">
            📌 채널 ID를 넣으면 채널의 정보를 볼 수 있어요! 그리고 키워드를 작성하면 키워드와 관련된 영상들이 추천 됩니다! ฅʕ •Ⱉ• ⠕ʔฅ
        </div>
    </div>
""", unsafe_allow_html=True)

# 🔲 좌측 사이드바 (고정 메뉴)
st.markdown("""
    <div style="width:200px; position:fixed; top:60px; left:0; height:100%; background:#fff; border-right:1px solid #ddd; padding:15px;">
        <p>🏠 홈</p>
        <p>🎬 Shorts</p>
        <p>📺 구독</p>
        <hr>
        <p>🎵 음악</p>
        <p>🎮 게임</p>
        <p>⚽ 스포츠</p>
    </div>
""", unsafe_allow_html=True)

# 🟥 메인 영역
st.markdown('<div style="margin-left:220px; padding:20px;">', unsafe_allow_html=True)

# 입력창
channel_id = st.text_input("🔑 채널 ID 입력", "")
keyword = st.text_input("🔍 키워드 입력", "")

# 채널 정보 출력
if channel_id:
    info = get_channel_info(channel_id)
    if info:
        st.markdown(f"""
            <div style="background:#fff; border-radius:15px; padding:20px; box-shadow:0 4px 10px rgba(0,0,0,0.1); margin-bottom:20px;">
                <img src="{info['thumbnail']}" style="border-radius:50%; width:100px;"><br>
                <h2>{info['title']}</h2>
                <p>👥 구독자 {info['subscribers']}명 | ▶ 영상 {info['videos']}개 | 👁️ 조회수 {info['views']}</p>
                <p>📝 {info['description']}</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.error("⚠️ 유효하지 않은 채널 ID입니다.")

# 키워드 관련 영상 출력
if keyword:
    videos = search_videos(keyword)
    if videos:
        st.markdown("<h2>🎥 추천 영상</h2>", unsafe_allow_html=True)
        cols = st.columns(3)
        for idx, video in enumerate(videos):
            with cols[idx % 3]:
                st.markdown(f"""
                    <div style="background:#fff; padding:10px; border-radius:10px; box-shadow:0 2px 5px rgba(0,0,0,0.1); margin-bottom:20px;">
                        <a href="https://www.youtube.com/watch?v={video['videoId']}" target="_blank">
                            <img src="{video['thumbnail']}" style="width:100%; border-radius:10px;">
                        </a>
                        <p>{video['title']}</p>
                    </div>
                """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
