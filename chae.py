import streamlit as st
from googleapiclient.discovery import build

# 페이지 설정
st.set_page_config(page_title="유튜브 채널 확인", page_icon="📺")

# 항상 화면에 표시되는 제목과 안내
st.title("유튜브 채널 구독자 확인")
st.write("채널 URL이 아니라 **채널 ID**(UC로 시작하는 ID)와 **API Key**를 입력해주세요.")

# 입력창
api_key = st.text_input("API Key 입력", type="password")
channel_id = st.text_input("채널 ID 입력", "UCp8knO8a6tSI1oaLjfd9XA")

# 입력이 되어야 동작
if api_key and channel_id:
    try:
        # YouTube API 객체 생성
        youtube = build('youtube', 'v3', developerKey=api_key)

        # 채널 정보 요청
        request = youtube.channels().list(
            part="snippet,statistics",
            id=channel_id
        )
        response = request.execute()

        # 채널 정보 가져오기
        channel_name = response['items'][0]['snippet']['title']
        subscribers = response['items'][0]['statistics']['subscriberCount']
        description = response['items'][0]['snippet']['description']

        # 결과 화면에 표시
        st.subheader("채널 정보")
        st.write(f"**채널 이름:** {channel_name}")
        st.write(f"**구독자 수:** {subscribers}명")
        st.write(f"**Description:** {description}")

    except Exception as e:
        # 실제 오류 메시지를 보여주어 문제 파악 가능
        st.error(f"⚠️ 채널 정보를 가져올 수 없습니다. 오류: {e}")
