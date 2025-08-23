import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

st.title("유튜브 채널 구독자 수 확인")

# URL 입력
channel_url = st.text_input("채널 URL을 입력하세요", "https://www.youtube.com/@kiatigerstv")

if channel_url:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    response = requests.get(channel_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text()

    match = re.search(r'([\d,.]+)\s*subscribers', text)
    if match:
        subscribers = match.group(1)
        st.write(f"구독자 수: {subscribers}")
    else:
        st.write("구독자 수를 찾을 수 없습니다.")
