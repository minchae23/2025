import streamlit as st
from googleapiclient.discovery import build
import requests
import re

# 페이지 설정
st.set_page_config(
    page_title="📺 유튜브 탐색기",
    page_icon="🎬",
    layout="wide"
)

# 배경색 스타일링
st.markdown(
    """
    <style>
    .stApp {background-color: #f9f9f9; color: #111;}
    .channel-card, .video-card {
        background-color: #fff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .video-container {display: flex; flex-wrap: wrap; gap: 15px;}
    .video-card img {width: 240px; height: 135px; border-radius: 6px;}
    </style>
    """, unsafe_allow_html=True
)

# 타이틀
st.markdown("<h2>📌 첫 번째 채널 ID만 넣으세요</h2>", unsafe_allow_html=True)
st.write("채널 ID를 입력하면 구독자 수와 채널 정보를 확인할 수 있어요!")

# 입력창
api_key = st.text_input("🔑 API Key 입력", type="password")
channel_input = st.text_input("💻 채널 ID를 입력하세요!", "UC_xxxxxxxx")

keyword_search = st.text_input("🔍 키워드 검색 (예: 오선우)")

def get_channel_id(channel_input):
    if channel_input.startswith("UC"):
        return channel_input
    match = re.search(r"@([a-zA-Z0-9_-]+)", channel_input)
    if match:
        username = match.group(1)
        url = f"https://www.googleapis.com/youtube/v3/channels?part=id&forUsername={username}&key={api_key}"
        try:
            response = requests.get(url).json()
            if 'items' in response and len(response['items']) > 0:
                return response['items'][0]['id']
            else:
                return None
        except:
            return None
    return None

if api_key and channel_input:
    channel_id = get_channel_id(channel_input)
    if not channel_id:
        st.error("⚠️ 유효하지 않은 채널입니다.")
    else:
        try:
            youtube = build('youtube', 'v3', developerKey=api_key)
            request = youtube.channels().list(part="snippet,statistics", id=channel_id)
            response = request.execute()

            if 'items' not in response or len(response['items']) == 0:
                st.error("⚠️ 채널 정보를 가져올 수 없습니다. 채널 ID를 확인해주세요.")
            else:
                channel_info = response['items'][0]
                channel_name = channel_info['snippet']['title']
                subscribers = channel_info['statistics']['subscriberCount']
                description = channel_info['snippet']['description']
                thumbnail = channel_info['snippet']['thumbnails']['high']['url']

                st.markdown('<div class="channel-card">', unsafe_allow_html=True)
                st.markdown(f"### 📺 {channel_name}")
                st.image(thumbnail, width=180)
                st.markdown(f"**👥 구독자 수:** {subscribers}명")
                st.markdown(f"**📝 Description:** {description}")
                st.markdown('</div>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"⚠️ 채널 정보를 가져오는 중 오류 발생: {e}")

# 키워드 검색
if api_key and keyword_search:
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        search_request = youtube.search().list(
            q=keyword_search,
            part="snippet",
            maxResults=12,
            type="video"
        )
        search_response = search_request.execute()

        if 'items' in search_response and len(search_response['items']) > 0:
            st.markdown("### 🔎 검색 결과")
            st.markdown('<div class="video-container">', unsafe_allow_html=True)
            for item in search_response['items']:
                video_id = item['id']['videoId']
                title = item['snippet']['title']
                channel_title = item['snippet']['channelTitle']
                thumbnail_url = item['snippet']['thumbnails']['medium']['url']
                st.markdown(
                    f'''
                    <div class="video-card">
                        <a href="https://www.youtube.com/watch?v={video_id}" target="_blank">
                            <img src="{thumbnail_url}">
                        </a>
                        <p><b>{title}</b></p>
                        <p>📺 {channel_title}</p>
                    </div>
                    ''', unsafe_allow_html=True
                )
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("검색 결과가 없습니다.")

    except Exception as e:
        st.error(f"⚠️ 키워드 검색 중 오류 발생: {e}")
