from googleapiclient.discovery import build
from youtube.api_key import build_youtube_with_fallback
from isodate import parse_duration
import time

youtube = build_youtube_with_fallback()

def update_video_meta_if_needed(video_ids, video_meta):
    new_ids = [vid for vid in video_ids if vid not in video_meta]
    print(f"[Meta] 메타데이터 수집 대상 영상 수: {len(new_ids)}")

    # YouTube API는 videos.list 최대 50개까지 batch 가능
    for i in range(0, len(new_ids), 50):
        batch = new_ids[i:i+50]
        try:
            response = youtube.videos().list(
                part="snippet,contentDetails",
                id=','.join(batch)
            ).execute()

            for item in response.get("items", []):
                vid = item["id"]
                snippet = item["snippet"]
                duration = item["contentDetails"]["duration"]
                seconds = parse_duration(duration).total_seconds()
                is_short = seconds <= 60

                video_meta[vid] = {
                    "title": snippet.get("title"),
                    "published_at": snippet.get("publishedAt"),
                    "thumbnail_url": snippet.get("thumbnails", {}).get("high", {}).get("url"),
                    "is_short": is_short
                }
                print(f"[Meta] 저장 완료: {vid} → {video_meta[vid]['title']}")

            time.sleep(1)

        except Exception as e:
            print(f"[Error] videos.list 호출 실패: {e}")
