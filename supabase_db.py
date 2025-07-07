import os
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def upsert_video(video_id, channel_id, title, published_at, is_short, thumbnail_url=None):
    data = {
        "id": video_id,
        "channel_id": channel_id,
        "title": title,
        "published_at": published_at,
        "is_short": is_short,
        "thumbnail_url": thumbnail_url
    }
    # 이미 있으면 무시, 없으면 삽입 (id 기준)
    supabase.table("videos").upsert(data, on_conflict=["id"]).execute()

def insert_video_snapshot(video_id, view_count, like_count, comment_count, subscriber_count, collected_at=None):
    if collected_at is None:
        collected_at = datetime.now().isoformat()
    data = {
        "video_id": video_id,
        "collected_at": collected_at,
        "view_count": view_count,
        "like_count": like_count,
        "comment_count": comment_count,
        "subscriber_count": subscriber_count
    }
    supabase.table("video_snapshots").insert(data).execute() 