import streamlit as st
import requests

# ---------------------------
# 🔑 API 키 (수정 불가, 경고 표시)
# ---------------------------
API_KEY = "AIzaSyCaL-ueb_PHj8j_4WgAol4thJMcwQF55Vc"
st.sidebar.markdown("### 🔑 API 키 (수정하지 마세요!)")
st.sidebar.text_input("API Key", API_KEY, type="password", disabled=True)

# ---------------------------
# 상단 로고 (중앙 고정)
# ---------------------------
st.markdown("""
    <div style="text-align:center; padding:15px; border-bottom:2px solid #eee;">
        <h1 style="color:red; font-size:36px; font-weight:bold;">▶ YouTube</h1>
    </div>
""", unsafe_allow_html=True)

# ---------------------------
# 사이드바 (고정 메뉴)
# ---------------------------
st.markdown("""
    <div style="width:220px; position:fixed; top:80px; left:0; height:100%; 
                background:#fff; border-right:1px solid #eee; padding:20px;">
        <p>🏠 홈</p>
        <p>🎬 Shorts</p>
        <p>📺 구독</p>
        <hr>
        <p>🎵 음악</p>
        <p>🎮 게임</p>
        <p>⚽ 스포츠</p>
    </div>
""", unsafe_allow_html=True)

# ---------------------------
# 본문 (사이드바 공간 확보)
# ---------------------------
st.markdown('<div style="margin-left:300px; padding:30px;">', unsafe_allow_html=True)

# 안내 문구 크게
st.markdown("""
    <h2 style="font-size:24px; font-weight:bold; color:#333;">
        📌 채널 ID를 넣으면 채널의 정보를 볼 수 있어요!<br>
        그리고 키워드를 작성하면 관련된 영상들이 추천됩니다! ฅʕ •Ⱉ• ⠕ʔฅ
    </h2>
""", unsafe_allow_html=True)

# ---------------------------
# 입력창
# ---------------------------
channel_id = st.text_input("🗝️ 채널 ID 입력")
keyword = st.text_input("🔎 키워드 입력")

# ---------------------------
# 채널 정보 가져오기
# ---------------------------
def get_channel_info(channel_id):
    url = f"https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&id={channel_id}&key={API_KEY}"
    response = requests.get(url).json()
    if "items" not in response or len(response["items"]) == 0:
        return None
    return response["items"][0]

# ---------------------------
# 키워드로 영상 검색
# ---------------------------
def search_videos(keyword):
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={keyword}&type=video&maxResults=6&key={API_KEY}"
    response = requests.get(url).json()
    if "items" not in response:
        return []
    return response["items"]

# ---------------------------
# 채널 정보 출력
# ---------------------------
if channel_id:
    info = get_channel_info(channel_id)
    if info:
        snippet = info["snippet"]
        stats = info["statistics"]

        st.image(snippet["thumbnails"]["high"]["url"], width=120)
        st.markdown(f"### 📺 {snippet['title']}")
        st.markdown(f"**설명:** {snippet['description']}")
        st.markdown(f"👥 구독자: {stats.get('subscriberCount', '비공개')}")
        st.markdown(f"▶ 영상 수: {stats.get('videoCount', 'N/A')}")
        st.markdown(f"👍 총 조회수: {stats.get('viewCount', 'N/A')}")
    else:
        st.error("⚠️ 유효하지 않은 채널 ID입니다.")

# ---------------------------
# 키워드 검색 결과 출력
# ---------------------------
if keyword:
    videos = search_videos(keyword)
    if videos:
        st.markdown("## 🔎 검색 결과")
        for video in videos:
            vid = video["id"]["videoId"]
            title = video["snippet"]["title"]
            thumb = video["snippet"]["thumbnails"]["medium"]["url"]

            st.image(thumb, width=250)
            st.markdown(f"[{title}](https://www.youtube.com/watch?v={vid})")
    else:
        st.warning("관련 영상을 찾을 수 없습니다.")

st.markdown('</div>', unsafe_allow_html=True)
