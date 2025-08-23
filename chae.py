import streamlit as st
from googleapiclient.discovery import build
import requests
import re

st.set_page_config(page_title="유튜브 채널 확인", page_icon="📺")
st.title("유튜브 채널 구독자 확인")
st.write("채널 URL 또는 채널 ID를 입력하면 채널 정보가 표시됩니다.")

# 입력창
api_key = st.text_input("API Key 입력", type="password")
channel_input = st.text_input("채널 URL 또는 ID 입력", "https://www.youtube.com/@kiatigerstv")

def get_channel_id(channel_input):
    """
    @사용자이름 또는 채널 URL을 실제 UC로 시작하는 채널 ID로 변환
    """
    # 이미 UC로 시작하면 그대로 반환
    if channel_input.startswith("UC"):
        return channel_input

    # @username 형태면 YouTube Data API로 ID 가져오기
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
        st.error("⚠️ 유효하지 않은 채널입니다. UC로 시작하는 채널 ID 또는 올바른 @사용자이름 입력 필요")
    else:
        try:
            youtube = build('youtube', 'v3', developerKey=api_key)
            request = youtube.channels().list(part="snippet,statistics", id=channel_id)
            response = request.execute()

            if 'items' not in response or len(response['items']) == 0:
                st.error("⚠️ 채널 정보를 가져올 수 없습니다. 채널 ID를 확인해주세요.")
            else:
                channel_name = response['items'][0]['snippet']['title']
                subscribers = response['items'][0]['statistics']['subscriberCount']
                description = response['items'][0]['snippet']['description']

                st.subheader("채널 정보")
                st.write(f"**채널 이름:** {channel_name}")
                st.write(f"**구독자 수:** {subscribers}명")
                st.write(f"**Description:** {description}")

        except Exception as e:
            st.error(f"⚠️ 채널 정보를 가져오는 중 오류 발생: {e}")
