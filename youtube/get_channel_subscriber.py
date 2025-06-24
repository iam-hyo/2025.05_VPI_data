from googleapiclient.discovery import build
from youtube.api_key import build_youtube_with_fallback
from datetime import datetime, timedelta

youtube = build_youtube_with_fallback()

# 구독자 수 캐시 (12시간 유지)
subscriber_cache = {}

def get_channel_subscriber_count(channel_id):
    now = datetime.now()

    # 12시간 내 캐시된 값이 있다면 그대로 사용
    cached = subscriber_cache.get(channel_id)
    if cached and (now - cached['timestamp']).total_seconds() < 43200:
        return cached['subscriber']

    try:
        request = youtube.channels().list(
            part="statistics",
            id=channel_id
        )
        response = request.execute()

        items = response.get('items', [])
        if items:
            subscriber_count = int(items[0]['statistics'].get('subscriberCount', 0))
            subscriber_cache[channel_id] = {
                "subscriber": subscriber_count,
                "timestamp": now
            }
            return subscriber_count
        else:
            print(f"[Warning] 구독자 수 조회 실패: 응답에 items 없음 (채널ID: {channel_id})")
            return 0
    except Exception as e:
        print(f"[Error] 구독자 수 조회 중 예외 발생 (채널ID: {channel_id}) → {e}")
        return 0
