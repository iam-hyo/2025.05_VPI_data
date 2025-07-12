# youtube_channel_collector.py

import os
from typing import List
from datetime import datetime
from youtube.api_key import build_youtube_with_fallback

from supabase import create_client, Client

# Supabase 설정
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

def get_channel_ids_from_supabase() -> List[str]:
    """Supabase에서 channel_id 리스트 반환"""
    response = supabase.table("channels").select("id").execute()
    return [item['id'] for item in response.data]

def fetch_and_store_channel_data(channel_ids: List[str]):
    """YouTube API로 채널 정보를 수집하고, Supabase에 트랜잭션으로 저장"""
    # 인증 및 클라이언트 생성
    youtube = build_youtube_with_fallback()

    # 트랜잭션 시작 (로컬 캐싱)
    updates_channels = []
    inserts_snapshots = []
    collected_at = datetime.now().isoformat()

    # 배치로 50개씩 API 호출
    for i in range(0, len(channel_ids), 50):
        batch_ids = channel_ids[i:i + 50]
        request = youtube.channels().list(
            part="snippet,contentDetails,statistics",
            id=",".join(batch_ids)
        )
        response = request.execute()

        for item in response.get("items", []):
            channel_id = item["id"]
            snippet = item.get("snippet", {})
            stats = item.get("statistics", {})

            # snapshot 저장용
            inserts_snapshots.append({
                "channel_id": channel_id,
                "collected_at": collected_at,
                "subscriber_count": int(stats.get("subscriberCount", 0)) if not stats.get("hiddenSubscriberCount") else None,
                "video_count": int(stats.get("videoCount", 0)),
                "total_view_count": int(stats.get("viewCount", 0)),
            })

            # channels_test 갱신용
            updates_channels.append({
                "id": channel_id,
                "title": snippet.get("title"),
                "description": snippet.get("description"),
                "profile_image": snippet.get("thumbnails", {}).get("default", {}).get("url"),
                "banner_image": snippet.get("thumbnails", {}).get("high", {}).get("url"),  # fallback
                "handle": snippet.get("customUrl"),
                "join_date": snippet.get("publishedAt"),
            })

    # 트랜잭션 적용
    try:
        # snapshot insert (여러 건)
        supabase.table("channel_snapshots").insert(inserts_snapshots).execute()

        # channel upsert
        supabase.table("channels").upsert(updates_channels, on_conflict=["id"]).execute()

    except Exception as e:
        print("🚨 저장 중 오류 발생! 모든 데이터 저장 중단됨")
        raise e