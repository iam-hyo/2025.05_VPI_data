# from googleapiclient.discovery import build
from youtube.api_key import build_youtube_with_fallback
import json
import os

# YouTube API build
youtube = build_youtube_with_fallback()

# ⚠️ 크레딧 명세서:
# - channels.list(part='snippet,brandingSettings') → 1 크레딧 / 1 채널 호출

# 채널 메타 정보 저장 경로
CHANNEL_META_PATH = 'data/channel_meta.json'

# 채널 리스트 JSON 경로를 사용자 정의로 입력받음
def update_channel_meta(json_path):
    with open(json_path, encoding='utf-8-sig') as f:
        channel_data = json.load(f)  # [{"channel_handle": ..., "channel_id": ..., "category": ...}]

    if os.path.exists(CHANNEL_META_PATH):
        with open(CHANNEL_META_PATH, encoding='utf-8-sig') as f:
            channel_meta = json.load(f)
    else:
        channel_meta = {}

    for ch in channel_data:
        cid = ch['channel_id']
        if cid in channel_meta:
            print(f"[Skip] 이미 저장된 채널: {ch['channel_handle']}")
            continue

        try:
            response = youtube.channels().list(
                part="snippet,brandingSettings,statistics",
                id=cid
            ).execute()

            item = response['items'][0]
            snippet = item['snippet']
            stats = item['statistics']
            branding = item.get('brandingSettings', {})
            banner = branding.get('image', {}).get('bannerExternalUrl')

            channel_meta[cid] = {
                "channel_title": snippet.get('title'),
                "channel_description": snippet.get('description'),
                "profile_image": snippet.get('thumbnails', {}).get('default', {}).get('url'),
                "banner_image": banner,
                "handle": ch.get('channel_handle'),
                "category": ch.get('category'),
                "video_count": int(stats.get('videoCount', 0)),
                "total_view_count": int(stats.get('viewCount', 0)),
                "join_date": snippet.get('publishedAt')
            }

            print(f"[Meta] 저장 완료: {ch['channel_handle']} ({cid})")

        except Exception as e:
            print(f"[Error] {ch['channel_handle']} 수집 실패: {e}")

    # 저장
    with open(CHANNEL_META_PATH, 'w', encoding='utf-8-sig') as f:
        json.dump(channel_meta, f, ensure_ascii=False, indent=2)

    print(f"[Done] 채널 메타정보 저장 완료 → {CHANNEL_META_PATH}")

if __name__ == "__main__":
    update_channel_meta('data/channels_full.json')

# 예시 호출
# update_channel_meta('data/channels_full.json')
