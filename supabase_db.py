from datetime import datetime
from supabase import create_client, Client
import os
from dotenv import load_dotenv

# 환경 변수 로딩
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# 유틸 함수: None 값 제거
def remove_none_fields(data: dict) -> dict:
    return {k: v for k, v in data.items() if v is not None}

# 영상 정보 upsert 함수
def upsert_video(video_id: str, channel_id: str, title: str, published_at, is_short: bool, thumbnail_url: str = None):
    if isinstance(published_at, datetime):
        published_at = published_at.strftime("%Y-%m-%dT%H:%M:%S")  # 'Z' 제거

    data = remove_none_fields({
        "id": video_id,
        "channel_id": channel_id,
        "title": title,
        "published_at": published_at,
        "is_short": is_short,
        "thumbnail_url": thumbnail_url
    })

    print(f"[DEBUG] upsert_video() 호출됨 - 데이터: {data}")
    try:
        response = supabase.table("videos").upsert(data, on_conflict=["id"]).execute()
        # print(f"[✅] upsert_video() 성공 - 응답: {response}")
    except Exception as e:
        print(f"[❌] upsert_video() 실패 - 오류: {e}")

# 스냅샷 정보 insert 함수
def insert_video_snapshot(video_id: str, view_count: int, like_count: int, comment_count: int, subscriber_count: int, collected_at=None):
    if collected_at is None:
        collected_at = datetime.now()
    if isinstance(collected_at, datetime):
        collected_at = collected_at.strftime("%Y-%m-%dT%H:%M:%S")  # 'Z' 제거

    data = remove_none_fields({
        "video_id": video_id,
        "collected_at": collected_at,
        "view_count": view_count,
        "like_count": like_count,
        "comment_count": comment_count,
        "subscriber_count": subscriber_count
    })

    print(f"[DEBUG] insert_video_snapshot() 호출됨 - 데이터: {data}")
    try:
        response = supabase.table("video_snapshots").insert(data).execute()
        # print(f"[✅] insert_video_snapshot() 성공 - 응답: {response}")
    except Exception as e:
        print(f"[❌] insert_video_snapshot() 실패 - 오류: {e}")