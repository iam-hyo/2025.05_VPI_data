# youtube/get_video_stats_batch.py

from googleapiclient.discovery import build
from youtube.api_key import build_youtube_with_fallback
from isodate import parse_duration

youtube = build_youtube_with_fallback()

def get_video_statistics_batch(video_ids):
    """
    영상 ID 목록을 최대 50개씩 묶어서 videos.list API로 한 번에 조회
    반환 형식: {video_id: (view, like, comment, is_short, published_at, title)}
    """
    results = {}
    for i in range(0, len(video_ids), 50):
        batch_ids = video_ids[i:i+50]
        response = youtube.videos().list(
            part='snippet,statistics,contentDetails',
            id=','.join(batch_ids)
        ).execute()

        for item in response.get('items', []):
            video_id = item['id']
            stats = item.get('statistics', {})
            snippet = item.get('snippet', {})
            duration = item.get('contentDetails', {}).get('duration', 'PT0S')

            seconds = parse_duration(duration).total_seconds()
            is_short = seconds <= 60

            results[video_id] = (
                int(stats.get('viewCount', 0)),
                int(stats.get('likeCount', 0)),
                int(stats.get('commentCount', 0)),
                is_short,
                snippet.get('publishedAt'),
                snippet.get('title')
            )
    return results
