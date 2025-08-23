import requests
from bs4 import BeautifulSoup
import re

# 채널 URL
channel_url = "https://www.youtube.com/@kiatigerstv"

# 페이지 가져오기
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}
response = requests.get(channel_url, headers=headers)

# HTML 파싱
soup = BeautifulSoup(response.text, "html.parser")

# 구독자 수 추출 (텍스트에서 'subscribers' 포함 검색)
text = soup.get_text()
match = re.search(r'([\d,.]+)\s*subscribers', text)

if match:
    subscribers = match.group(1)
    print(f"구독자 수: {subscribers}")
else:
    print("구독자 수를 찾을 수 없습니다.")
