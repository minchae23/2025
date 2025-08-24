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
<div style="width:220px;position:fixed;top:60px;left:0;height:100%;background:#fff;border-right:1px solid #eee;padding:12px 10px;">
  <p>🏠 홈</p>
  <p>🎬 Shorts</p>
  <p>📺 구독</p>
  <hr>
  <p>🎵 음악</p>
  <p>🎮 게임</p>
  <p>⚽ 스포츠</p>
</div>
""", unsafe_allow_html=True)

# 본문: 사이드바와 겹치지 않게 여백 확보
st.markdown('<div style="margin-left:260px;padding:20px;">', unsafe_allow_html=True)

# ✅ 입력창은 항상 고정(사라지지 않음)
channel_id = st.text_input("🔑 채널 ID 입력", "")
keyword = st.text_input("🔍 키워드 입력", "")

# 채널 정보
if channel_id:
    info = get_channel_info(channel_id)  # <-- 괄호 완전하게!
    if info:
        st.markdown(
            f"""
            <div style="background:#fff;border-radius:14px;padding:20px;box-shadow:0 4px 10px rgba(0,0,0,.08);margin:10px 0 24px;">
              <img src="{info['thumbnail']}" style="border-radius:50%;width:96px;height:96px;object-fit:cover;"><br>
              <h2 style="margin:10px 0 6px;">{info['title']}</h2>
              <p>👥 {info['subscribers']}명 · ▶ {info['videos']}개 · 👁️ {info['views']}</p>
              <p style="white-space:pre-wrap;">{info['description']}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.error("⚠️ 유효하지 않은 채널 ID입니다.")

# 키워드 검색 결과
if keyword:
    vids = search_videos(keyword, max_results=9)
    if vids:
        st.markdown("<h3 style='margin-top:0;'>🎥 추천 영상</h3>", unsafe_allow_html=True)
        cols = st.columns(3)
        for i, v in enumerate(vids):
            with cols[i % 3]:
                st.markdown(
                    f"""
                    <div style="background:#fff;padding:10px;border-radius:10px;box-shadow:0 2px 6px rgba(0,0,0,.06);margin-bottom:18px;">
                      <a href="https://www.youtube.com/watch?v={v['videoId']}" target="_blank">
                        <img src="{v['thumbnail']}" style="width:100%;border-radius:8px;">
                      </a>
                      <p style="margin:8px 0 4px;font-weight:600;">{v['title']}</p>
                      <p style="margin:0;color:#666;">📺 {v['channelTitle']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    else:
        st.info("검색 결과가 없습니다.")

st.markdown("</div>", unsafe_allow_html=True)
