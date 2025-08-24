import streamlit as st
import requests

st.set_page_config(layout="wide", page_title="YouTube Info Viewer", page_icon="▶")

# 고정 API 키
API_KEY = "AIzaSyCaL-ueb_PHj8j_4WgAol4thJMcwQF55Vc"

def get_channel_info(channel_id):
    url = f"https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&id={channel_id}&key={API_KEY}"
    r = requests.get(url).json()
    if "items" not in r or not r["items"]:
        return None
    it = r["items"][0]
    sn, stc = it["snippet"], it["statistics"]
    return {
        "title": sn["title"],
        "description": sn.get("description", ""),
        "thumbnail": sn["thumbnails"]["high"]["url"],
        "subscribers": stc.get("subscriberCount", "0"),
        "videos": stc.get("videoCount", "0"),
        "views": stc.get("viewCount", "0"),
    }

def search_videos(q, max_results=6):
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&q={q}&maxResults={max_results}&key={API_KEY}"
    r = requests.get(url).json()
    vids = []
    for it in r.get("items", []):
        vids.append({
            "title": it["snippet"]["title"],
            "thumbnail": it["snippet"]["thumbnails"]["high"]["url"],
            "videoId": it["id"]["videoId"],
            "channelTitle": it["snippet"]["channelTitle"],
        })
    return vids

# 헤더
st.markdown("""
<div style="display:flex;align-items:center;justify-content:space-between;padding:10px 16px;border-bottom:1px solid #e5e5e5;background:#fff;position:sticky;top:0;z-index:10;">
  <div style="font-size:24px;font-weight:700;color:#ff0000;">▶ YouTube</div>
  <div style="font-size:16px;font-weight:600;">📌 채널 ID를 넣으면 채널의 정보를 볼 수 있어요! 그리고 키워드를 작성하면 키워드와 관련된 영상들이 추천 됩니다! ฅʕ •Ⱉ• ⠕ʔฅ</div>
</div>
""", unsafe_allow_html=True)

# 사이드바(고정)
st.markdown("""
<div style
