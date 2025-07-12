# youtube_video_collector.py

import os
import isodate
from datetime import datetime
from typing import List, Dict
from youtube.api_key import build_youtube_with_fallback


from supabase import create_client, Client

# Supabase 설정
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

def fetch_videos_from_channel(channel_id: str) -> List[Dict]:
    youtube = build_youtube_with_fallback()

    # Step 1: upload playlist ID 얻기
    channel_response = youtube.channels().list(
        part="contentDetails",
        id=channel_id
    ).execute()

    uploads_playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    # Step 2: 영상 50개 가져오기
    playlist_response = youtube.playlistItems().list(
        part="snippet,contentDetails",
        playlistId=uploads_playlist_id,
        maxResults=50
    ).execute()

    video_ids = [item["contentDetails"]["videoId"] for item in playlist_response["items"]]

    # Step 3: video statistics 포함된 video 상세 정보 얻기
    videos_response = youtube.videos().list(
        part="snippet,statistics,contentDetails",
        id=",".join(video_ids)
    ).execute()

    return videos_response["items"]

def parse_duration_to_seconds(duration_str: str) -> int:
    """ISO 8601 duration → 초 단위 정수 변환"""
    try:
        duration = isodate.parse_duration(duration_str)
        return int(duration.total_seconds())
    except Exception:
        return 0

def store_videos_and_snapshots(channel_id: str, videos: List[Dict]):
    collected_at = datetime.utcnow().isoformat()
    video_records = []
    snapshot_records = []

    for video in videos:
        vid = video["id"]
        snippet = video["snippet"]
        stats = video.get("statistics", {})
        content_details = video.get("contentDetails", {})
        duration_str = content_details.get("duration", "")
        duration_seconds = parse_duration_to_seconds(duration_str)
        
        video_records.append({
            "id": vid,
            "channel_id": channel_id,
            "title": snippet.get("title"),
            "published_at": snippet.get("publishedAt"),
            "is_short": duration_seconds <= 140,  # 140초 이하이면 Shorts
            "thumbnail_url": snippet.get("thumbnails", {}).get("default", {}).get("url")
        })

        snapshot_records.append({
            "video_id": vid,
            "collected_at": collected_at,
            "view_count": int(stats.get("viewCount", 0)),
            "like_count": int(stats.get("likeCount", 0)),
            "comment_count": int(stats.get("commentCount", 0))
        })

    try:
        # 영상 업서트
        supabase.table("videos").upsert(video_records, on_conflict=["id"]).execute()

        # snapshot 저장
        supabase.table("video_snapshots").insert(snapshot_records).execute()

    except Exception as e:
        print("🚨 영상 또는 snapshot 저장 실패! 전체 작업 중단")
        raise e
