import os
from typing import List
from datetime import datetime
from youtube.api_key import build_youtube_with_fallback

from supabase import create_client, Client

# Supabase 설정
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

class ChannelAdmin:
    def __init__(self, handle: str, channel_id: str, category: str):
        self.handle = handle
        self.channel_id = channel_id
        self.category = category

def fetch_channel_admin_list() -> List[ChannelAdmin]:
    response = supabase.table("channel_admin_test").select("*").execute()
    return [ChannelAdmin(row["channel_handle"], row["channel_id"], row["category"]) for row in response.data]

def initialize_channels_from_admins(channel_admins: List[ChannelAdmin]):
    youtube = build_youtube_with_fallback()

    channel_ids = [admin.channel_id for admin in channel_admins]

    results = []
    for i in range(0, len(channel_ids), 50):  # API 제한에 따라 50개 단위로 조회
        batch_ids = channel_ids[i:i + 50]
        response = youtube.channels().list(
            part="snippet,brandingSettings",
            id=",".join(batch_ids)
        ).execute()

        for item in response.get("items", []):
            cid = item["id"]
            snippet = item.get("snippet", {})
            branding = item.get("brandingSettings", {})
            image_banner = branding.get("image", {}).get("bannerExternalUrl")
            matching_admin = next((admin for admin in channel_admins if admin.channel_id == cid), None)

            results.append({
                "id": cid,
                "title": snippet.get("title"),
                "description": snippet.get("description"),
                "profile_image": snippet.get("thumbnails", {}).get("default", {}).get("url"),
                "banner_image": image_banner,
                "handle": matching_admin.handle if matching_admin else None,
                "category": matching_admin.category if matching_admin else None,
                "join_date": snippet.get("publishedAt")
            })

    # Supabase upsert
    try:
        supabase.table("channels_test").upsert(results, on_conflict=["id"]).execute()
    except Exception as e:
        print("🚨 채널 저장 실패:", e)
        raise e