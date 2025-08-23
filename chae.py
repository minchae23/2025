from googleapiclient.discovery import build

# 1️⃣ 여기에 발급받은 API Key 입력
api_key = "여기에_API_KEY"

# 2️⃣ 여기에 채널 ID 입력 (UC로 시작)
channel_id = "UCp8knO8a6tSI1oaLjfd9XA"

try:
    # 3️⃣ YouTube API 객체 생성
    youtube = build('youtube', 'v3', developerKey=api_key)

    # 4️⃣ 채널 정보 요청
    request = youtube.channels().list(
        part="snippet,statistics",
        id=channel_id
    )
    response = request.execute()

    # 5️⃣ 결과 출력
    channel_name = response['items'][0]['snippet']['title']
    subscribers = response['items'][0]['statistics']['subscriberCount']
    description = response['items'][0]['snippet']['description']

    print("===== 채널 정보 =====")
    print(f"채널 이름: {channel_name}")
    print(f"구독자 수: {subscribers}명")
    print(f"Description: {description}")

except Exception as e:
    print("⚠️ 채널 정보를 가져올 수 없습니다. 오류:", e)
