
import os
from flask import Flask, render_template, jsonify
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Flask 앱 설정
app = Flask(__name__)

# 환경 변수 로드
load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")

# 유튜브 API 클라이언트 초기화
youtube = build("youtube", "v3", developerKey=API_KEY)

# 유튜브 채널 ID (강환국 채널)
CHANNEL_ID = "UC5gB48k0RzG3T18_m1HlKfw"

# 최신 영상 확인 함수
def get_latest_video():
    request = youtube.activities().list(
        part="snippet",
        channelId=CHANNEL_ID,
        maxResults=1,
        publishedAfter=(datetime.now() - timedelta(days=1)).isoformat() + "Z"
    )
    response = request.execute()
    
    if "items" in response:
        latest_video = response["items"][0]
        video_title = latest_video["snippet"]["title"]
        video_url = "https://www.youtube.com/watch?v=" + latest_video["snippet"]["resourceId"]["videoId"]
        return video_title, video_url
    else:
        return None, None

# 영상 요약 (한 줄로 수정)
def summarize_video(title, url):
    summary = f"New Video: {title}
Link: {url}

Summary:
1. The video discusses the latest trends in crypto.
2. Insights on market fluctuations and predictions."
    return summary

# 기본 웹 페이지
@app.route('/')
def index():
    video_title, video_url = get_latest_video()
    if video_title and video_url:
        summary = summarize_video(video_title, video_url)
        return render_template('index.html', summary=summary)
    else:
        return render_template('index.html', summary="No new video found in the last 24 hours.")

if __name__ == '__main__':
    app.run(debug=True)
