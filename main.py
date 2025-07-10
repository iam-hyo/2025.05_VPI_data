import os
import json
import pandas as pd
from datetime import datetime
import logging

from youtube.get_video_stats import get_video_statistics_batch
from youtube.get_video_meta import update_video_meta_if_needed
from youtube.get_channel_subscriber import get_channel_subscriber_count
from youtube.get_video_id_byPlaylist import get_recent_video_ids_max_50
from supabase_db import upsert_video, insert_video_snapshot

logging.basicConfig(
    filename="01_VPI_data/logs/log.txt",
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')  # '/home/hjj/02_VPI_app/data'
os.makedirs(DATA_DIR, exist_ok=True) # 디렉터리 없으면 생성

print(f"[🕒] 현재 시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# 채널 정보 로딩 (handle, id, category 포함)
CHANNELS_PATH = os.path.join(DATA_DIR, 'channels_full.json')
with open(CHANNELS_PATH, encoding='utf-8-sig') as f:
    channels = json.load(f)

# 비디오 메타 캐시 로딩
VIDEO_META_PATH = os.path.join(DATA_DIR, 'video_meta.json')
if os.path.exists(VIDEO_META_PATH) and os.stat(VIDEO_META_PATH).st_size > 0:
    with open(VIDEO_META_PATH, encoding='utf-8-sig') as f:
        video_meta = json.load(f)
else:
    video_meta = {}

def fetch_and_save_data():
    all_data = []
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')

    for channel in channels:
        handle = channel['channel_handle']
        category = channel['category']
        channel_id = channel['channel_id']

        subscriber_count = get_channel_subscriber_count(channel_id)

        video_ids = get_recent_video_ids_max_50(channel_id, max_results=50)

        try:
            video_stats_dict = get_video_statistics_batch(video_ids)
        except Exception as e:
            print(f"[Error] 영상 통계 조회 실패: {e}")
            continue
        update_video_meta_if_needed(video_ids, video_meta)

        for video_id in video_ids:
            if video_id not in video_stats_dict:
                print(f"[Warning] 영상 통계 누락: {video_id}")
                continue

            view_count, like_count, comment_count, is_short, published_at, video_title = video_stats_dict[video_id]            
            meta = video_meta.get(video_id, {})
            thumbnail_url = meta.get("thumbnail_url")

            record = {
                "timestamp": timestamp,
                "category": category,
                "channel_id": channel_id,
                "channel_handle": handle,
                "video_id": video_id,
                "video_title": meta.get("title"),
                "published_at": meta.get("published_at"),
                "is_short": meta.get("is_short"),
                "view_count": view_count,
                "like_count": like_count,
                "comment_count": comment_count,
                "subscriber_count": subscriber_count,
                "thumbnail_url": thumbnail_url,
            }
            all_data.append(record)

            # Supabase DB 저장
            upsert_video(
                video_id=video_id,
                channel_id=channel_id,
                title=video_title,
                published_at=published_at,
                is_short=is_short,
                thumbnail_url= thumbnail_url
            )
            insert_video_snapshot(
                video_id=video_id,
                view_count=view_count,
                like_count=like_count,
                comment_count=comment_count,
                subscriber_count=subscriber_count,
                collected_at=timestamp
            )
            print(f"[Info] 수집 완료: {handle}, 영상ID: {video_id}")

    # CSV 저장
    csv_file = os.path.join(DATA_DIR, 'processed_data_v2.csv')
    df = pd.DataFrame(all_data)
    df['video_id'] = df['video_id'].apply(lambda x: f"'{x}" if isinstance(x, str) and (x.startswith('=') or x.startswith('-')) else x)
    if os.path.exists(csv_file):
        df.to_csv(csv_file, mode='a', index=False, header=False, encoding='utf-8-sig')
    else:
        df.to_csv(csv_file, index=False, encoding='utf-8-sig')

    logging.info(f"데이터 저장 완료: {timestamp}")
    print("실행 끝")

if __name__ == "__main__":
    try:
        logging.info("======== 유튜브 채널 수집 실행 시작 ========")
        fetch_and_save_data()
        logging.info("======== 실행 완료 ========")
    except Exception as e:
        logging.error(f"[Fatal Error] 데이터 수집 전체 실패: {e}", exc_info=True)