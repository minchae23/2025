import streamlit as st
import requests

# ---------------------------
# 🔑 API 키 (숨김, 수정 불가)
# ---------------------------
API_KEY = "AIzaSyCaL-ueb_PHj8j_4WgAol4thJMcwQF55Vc"

# ---------------------------
# 📌 유튜브 API 함수
# ---------------------------
def get_channel_info(channel_id):
    url = f"https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&id={channel_id}&key={API_KEY}"
    res = requests.get(url).json()
    if "items" not in res or len(res["items"]) == 0:
        return None
    item = res["items"][0]
    return {
        "title": item["snippet"]["title"],
        "description": item["snippet"]["description"],
        "thumbnail": item["snippet"]["thumbnails"]["high"]["url"],
        "subscribers": item["statistics"].get("subscriberCount", "0"),
        "videos": item["statistics"].get("videoCount", "0"),
    }

def search_videos(keyword):
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={keyword}&maxResults=10&type=video&key={API_KEY}"
    res = requests.get(url).json()
    return res.get("items", [])

# ---------------------------
# 🎨 UI 꾸미기
# ---------------------------
st.set_page_config(page_title="YouTube Info", layout="wide")

# ✅ 사이드바 (유튜브 메뉴)
with st.sidebar:
    st.markdown("### 📺 메뉴")
    st.markdown("🏠 홈")
    st.markdown("🎬 Shorts")
    st.markdown("📂 구독")
    st.markdown("---")
    st.markdown("🎵 음악")
    st.markdown("🎮 게임")
    st.markdown("⚽ 스포츠")

# ✅ 상단 로고
st.markdown("<h1 style='text-align:center; color:red;'>▶ YouTube</h1>", unsafe_allow_html=True)
st.markdown("---")

# ✅ 안내 문구
st.markdown(
    "<h3>📌 채널 ID를 넣으면 채널의 정보를 볼 수 있어요!<br>"
    "그리고 키워드를 작성하면 키워드와 관련된 영상들이 추천됩니다! ฅʕ •Ⱉ• ⠕ʔฅ</h3>",
    unsafe_allow_html=True
)

# ✅ 입력창 (본문)
channel_id = st.text_input("🔑 채널 ID 입력")
keyword = st.text_input("🔍 키워드 입력")

# ✅ 채널 정보 출력
if channel_id:
    info = get_channel_info(channel_id)
    if info:
        st.image(info["thumbnail"], width=150)
        st.subheader(info["title"])
        st.write(info["description"])
        st.write(f"👥 구독자 수: {info['subscribers']}")
        st.write(f"🎥 업로드 영상 수: {info['videos']}")
    else:
        st.error("⚠️ 유효하지 않은 채널 ID 입니다.")

# ✅ 키워드 검색 결과 출력
if keyword:
    videos = search_videos(keyword)
    st.subheader(f"🔎 '{keyword}' 관련 영상")
    for v in videos:
        vid_id = v["id"]["videoId"]
        title = v["snippet"]["title"]
        thumb = v["snippet"]["thumbnails"]["medium"]["url"]
        st.image(thumb, width=200)
        st.markdown(f"[{title}](https://www.youtube.com/watch?v={vid_id})")
