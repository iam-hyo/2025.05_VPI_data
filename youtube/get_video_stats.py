# youtube/get_video_stats_batch.py

from googleapiclient.discovery import build
from youtube.api_key import build_youtube_with_fallback
from isodate import parse_duration
from googleapiclient.errors import HttpError

youtube = build_youtube_with_fallback()

def get_video_statistics_batch(video_ids):
    results = {}
    for i in range(0, len(video_ids), 50):
        batch_ids = video_ids[i:i+50]
        try:
            response = youtube.videos().list(
                part='snippet,statistics,contentDetails',
                id=','.join(batch_ids)
            ).execute()

            items = response.get('items', [])
            if not items:
                print(f"[Warning] items 응답 없음 (video_ids: {batch_ids})")
                continue

            for item in items:
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
        except HttpError as e:
            print(f"[API 오류] videos.list 실패: {e}")
        except Exception as e:
            print(f"[예상 외 오류] {e}")
    return results
