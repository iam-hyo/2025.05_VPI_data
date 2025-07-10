# youtube/get_video_id_byPlaylist.py
from googleapiclient.discovery import build
from youtube.api_key import build_youtube_with_fallback
from datetime import datetime, timedelta
import json

youtube = build_youtube_with_fallback()

def get_uploads_playlist_id(channel_id):
    request = youtube.channels().list(
        part='contentDetails',
        id=channel_id
    )
    response = request.execute()

    items = response.get('items', [])
    if items:
        uploads_playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        return uploads_playlist_id
    print("[DEBUG] items가 비어 있습니다. 응답 전체:\n", json.dumps(response, indent=2))
    return None

def get_recent_video_ids_max_50(channel_id, channel_handle="", max_results=50):
    """
    해당 채널의 최신 업로드 영상 ID를 최대 max_results개까지 수집
    - 채널 ID를 통해 uploads playlist ID를 얻고
    - playlistItems.list를 반복 호출해 영상 ID를 최대 50개까지 추출
    - channel_handle이 제공되면 로그에 함께 출력

    ✅ 크레딧 소모량: playlistItems.list → 1 크레딧 / 최대 50개
    """
    playlist_id = get_uploads_playlist_id(channel_id)
    if not playlist_id:
        print(f"[Error] uploads playlist ID 조회 실패: {channel_id}")
        return []

    video_ids = []
    next_page_token = None

    while len(video_ids) < max_results:
        request = youtube.playlistItems().list(
            part='contentDetails',
            playlistId=playlist_id,
            maxResults=min(50, max_results - len(video_ids)),
            pageToken=next_page_token
        )
        response = request.execute()
        items = response.get('items', [])

        for item in items:
            video_ids.append(item['contentDetails']['videoId'])
            if len(video_ids) >= max_results:
                break

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    print(f"[Info] {channel_handle or channel_id} → 영상 {len(video_ids)}개 수집 완료", flush=True)
    return video_ids